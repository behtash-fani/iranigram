from django.utils.translation import gettext_lazy as _
from orders.tasks import send_submit_order_sms_task
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from orders.views import finish_payment
from django.contrib import messages
from django.conf import settings
import requests
import json
from orders.models import Order

def payment_request(request):
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
                request.session["status"] = False
                messages.error(
                    request,
                    _(
                        "Unfortunately, the connection with the bank portal was not established. The technical team will fix this problem as soon as possible"
                    ),
                    "danger",
                )
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
        request.session["status"] = False
        return redirect("callback_gateway")


def payment_verify(request):
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
            if payment_purpose == "pay_order_online":
                user = request.user
                if "use_wallet_status" in request.session and request.session["use_wallet_status"]:
                    order_id = request.session["order_id"]
                    order = Order.objects.get(id=order_id)
                    user.balance = (online_paid_amount+user.balance) - order.amount
                    user.save()
                finish_payment(
                    request,
                    payment_method="online",
                    trans_type="payment_for_order"
                )
                send_submit_order_sms_task.delay(user.phone_number, order.order_code)
                return redirect("callback_gateway")
            else:
                context = {"payment_purpose": "error"}
                return render(request, "accounts/callback_gateway.html", context)
        else:
            request.session["status"] = False
            return redirect("callback_gateway")

    return redirect("callback_gateway")