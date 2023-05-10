from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from transactions.models import Transactions
from django.conf import settings
from accounts.models import User
from orders.models import Order
from django.shortcuts import get_object_or_404
import requests
import json
from django.contrib import messages


def payment_request(request):
    phone = request.session["phone_number"]
    amount = request.session["amount"]
    transaction_detail = str(request.session["transaction_detail"][0])
    CallbackURL = f'{settings.SITE_URL}/payment-verify/'
    description = transaction_detail
    req_data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "CallbackURL": CallbackURL,
        "Description": description,
        "metadata": {"mobile": phone}
    }
    data = json.dumps(req_data)
    headers = {'content-type': 'application/json',
               'content-length': str(len(data))}
    try:
        print(CallbackURL)
        req = requests.post(url=settings.ZP_API_REQUEST,
                            data=data, headers=headers, timeout=10)
        if 'meta' in req.json():
            if req.json()['meta']['code'] == 404:
                request.session['status'] = False
                messages.error(
                    request,
                    _('Unfortunately, the connection with the bank portal was not established. The technical team will fix this problem as soon as possible'),
                    'danger')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if req.status_code == 200:
            authority = req.json()['Authority']
            if req.json()['Status'] == 100:
                return redirect(settings.ZP_API_STARTPAY + str(authority))
            else:
                request.session['status'] = False
                return redirect('callback_gateway')
        return req.json()

    except requests.exceptions.Timeout:
        request.session['status'] = False
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except requests.exceptions.ConnectionError:
        request.session['status'] = False
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print(e)
        request.session['status'] = False
        return redirect('callback_gateway')


def payment_verify(request):
    authority = request.GET['Authority']
    amount = request.session["amount"]
    phone = request.session["phone_number"]
    user = User.objects.get(phone_number=phone)
    if "order_id" in request.session:
        order_id = request.session["order_id"]
    payment_type = request.session["payment_type"]
    transaction_detail = str(request.session["transaction_detail"][0])
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    headers = {"accept": "application/json",
               "content-type": "application/json'"}
    req = requests.post(settings.ZP_API_VERIFY,
                        data=data, headers=headers)

    if req.status_code == 200: # successful payment
        if req.json()['Status'] == 100: 
            request.session['status'] = True
            if payment_type == 'pay_order_online':
                if 'order_id' in request.session:
                    order_id = request.session["order_id"]
                    order = get_object_or_404(Order, id=order_id)
                    order.wallet_paid_amount = 0
                    order.online_paid_amount = amount
                    order.status = 'Queued'
                    order.paid = True
                    order.save()
                    Transactions.objects.create(
                        user=user,
                        type="payment_for_order",
                        price=amount,
                        balance=user.balance,
                        payment_type="online",
                        details=transaction_detail,
                        order_code=order.order_code,
                        payment_gateway=_('Zarinpal'),
                        ip=request.META.get('REMOTE_ADDR'))
                else:
                    context = {'payment_type': 'error'}
                    return render(request,'accounts/callback_gateway.html',context)
                return redirect('callback_gateway')
            elif payment_type == 'add_fund_wallet':
                user.balance += amount
                user.save()
                Transactions.objects.create(user=user,
                                            type="add_fund",
                                            price=amount,
                                            balance=user.balance,
                                            payment_type="online",
                                            details=_('Increase wallet credit'),
                                            payment_gateway=_('Zarinpal'),
                                            ip=request.META.get('REMOTE_ADDR'))
                return redirect('callback_gateway')
            elif payment_type == 'pay_remain_price':
                total_order_price = request.session['total_order_price']
                order = get_object_or_404(Order, id=order_id)
                order.paid = True
                total_amount = user.balance + amount
                order.wallet_paid_amount = user.balance
                user.balance = 0
                remain_amount = total_amount - total_order_price
                user.balance += remain_amount
                order.online_paid_amount = amount - remain_amount
                order.status = "Queued"
                user.save()
                order.save()
                Transactions.objects.create(
                    user=user,
                    type="payment_for_order",
                    price=amount,
                    balance=user.balance,
                    payment_type="online",
                    details=transaction_detail,
                    order_code=order.order_code,
                    payment_gateway=_('Zarinpal'),
                    ip=request.META.get('REMOTE_ADDR'))
                return redirect('callback_gateway')
        else:
            request.session['status'] = False
            return redirect('callback_gateway')
    return req
