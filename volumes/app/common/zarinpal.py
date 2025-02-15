from django.utils.translation import gettext_lazy as _
from transactions.models import Transactions as Trans
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from orders.views import finish_payment
from django.contrib import messages
from django.conf import settings
from orders.models import Order
from decouple import config
import requests
import logging
import json

logger = logging.getLogger(__name__)

def zarinpal_payment_request(request):
    phone = request.session["phone_number"]
    amount_payable = request.session["amount_payable"]
    CallbackURL = f"{settings.SITE_URL}/payment-verify/"
    description = str(_("Online payment of the order fee"))
    req_data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount_payable,
        "CallbackURL": CallbackURL,
        "Description": description,
        "Mobile": f"{phone}",
    }
    data = json.dumps(req_data)
    headers = {"content-type": "application/json", "content-length": str(len(data))}
    try:
        req = requests.post(
            url=settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10
        )
        if "meta" in req.json():
            if req.json()["meta"]["code"] == 404:
                messages.error(
                    request,
                    _(
                        "Unfortunately, the connection with the bank portal was not established. The technical team will fix this problem as soon as possible"
                    ),
                    "danger",
                )
                request.session["status"] = False
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        if req.status_code == 200:
            authority = req.json()["Authority"]
            if req.json()["Status"] == 100:
                return redirect(settings.ZP_API_STARTPAY + str(authority))
            else:
                request.session["status"] = False
                return redirect("callback_gateway")
        return req.json()

    except requests.exceptions.Timeout:
        request.session["status"] = False
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    except requests.exceptions.ConnectionError:
        request.session["status"] = False
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    except Exception as e:
        logger.error(e)
        request.session["status"] = False
        return redirect("callback_gateway")


def zarinpal_payment_verify(request):
    authority = request.GET.get("Authority")
    online_paid_amount = request.session.get("amount_payable")
    payment_purpose = request.session.get("payment_purpose")

    if not authority or not online_paid_amount or not payment_purpose:
        # Handle missing parameters as needed
        context = {"payment_purpose": "error"}
        return render(request, "accounts/callback_gateway.html", context)

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": online_paid_amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    headers = {"accept": "application/json", "content-type": "application/json"}
    req = requests.post(settings.ZP_API_VERIFY, data=data, headers=headers)

    if req.status_code == 200:  # successful payment
        if req.json()["Status"] == 100:
            request.session["status"] = True
            user = request.user
            if payment_purpose == "pay_order_online":
                if int(online_paid_amount) < 1000:
                    online_paid_amount = 1000
                    order_id = request.session["order_id"]
                    order = Order.objects.get(id=order_id)
                    additional_amount = online_paid_amount - order.amount
                    user.balance += additional_amount
                    user.save()
                    Trans.objects.create(user=user,
                                        type="add_fund",
                                        price=additional_amount,
                                        balance=user.balance,
                                        payment_type="online",
                                        details="مبلغ اضافه پرداخت شده",
                                        order_code="--",
                                        payment_gateway=_('Vandar'),
                                        ip=request.META.get('REMOTE_ADDR'))
                finish_payment(
                    request,
                    payment_method="online",
                    trans_type="payment_for_order"
                )
                request.session["status"] = True
                return redirect("callback_gateway")
            elif payment_purpose == "add_fund_wallet":
                user.balance += online_paid_amount
                user.save()
                Trans.objects.create(user=user,
                                            type="add_fund",
                                            price=online_paid_amount,
                                            balance=user.balance,
                                            payment_type="online",
                                            details=_('Increase wallet credit'),
                                            order_code="--",
                                            payment_gateway=_('Zarinpal'),
                                            ip=request.META.get('REMOTE_ADDR'))
                request.session["status"] = True
                return redirect('callback_gateway')
            else:
                context = {"payment_purpose": "error"}
                return render(request, "accounts/callback_gateway.html", context)
        else:
            request.session["status"] = False
            return redirect("callback_gateway")

    return redirect("callback_gateway")