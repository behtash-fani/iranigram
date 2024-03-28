from django.utils.translation import gettext_lazy as _
from transactions.models import Transactions as Trans
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from orders.views import finish_payment
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from orders.models import Order
from bs4 import BeautifulSoup
import requests
import logging
from decouple import config
import json

logger = logging.getLogger(__name__)
access_token = config("VANDAR_ACCESS_TOKEN")
api_token = config("VANDAR_API_TOKEN")

def vandar_payment_request(request):
	try:
		payment_request_endpoint = "https://ipg.vandar.io/api/v3/send"
		phone = request.session["phone_number"]
		amount_payable = request.session["amount_payable"]
		if amount_payable < 1000:
			amount_payable = 1000
		CallbackURL = f"{settings.SITE_URL}/payment-verify/"
		description = str(_("Online payment of the order fee"))
		amount = int(f"{amount_payable}0")
		payload = json.dumps({
			"api_key": f'{api_token}',
			"amount": amount,
			"callback_url": CallbackURL,
			"mobile_number": phone,
			"description": description
		})
		headers = {
			'Accept': 'application/json',
			'Content-Type': 'application/json',
			'Authorization': f"Bearer {access_token}"
		}
		response = requests.request(
			"POST", payment_request_endpoint, headers=headers, data=payload)
		response_json = json.loads(response.text)
		payment_status = response_json.get('status', None)
		payment_token = response_json.get('token', None)
		request.session["token"] = payment_token
	except requests.exceptions.Timeout:
		return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
	except requests.exceptions.ConnectionError:
		return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
	except Exception as e:
		logger.error(e)
		return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

	try:
		if payment_status == 1:
			gateway_endpoint = f"https://ipg.vandar.io/v3/{payment_token}"
			gateway_payload = ""
			gateway_headers = {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
			}
			response = requests.request(
				"GET", gateway_endpoint, headers=gateway_headers, data=gateway_payload)
			html_response = response.content.decode('utf-8')
			soup = BeautifulSoup(html_response, 'html.parser')
			script_tag = soup.find('script')
			if script_tag:
				window_location = script_tag.string.strip().split("'")[1]
				return redirect(window_location)
		else:
			request.session["status"] = False
			return redirect("callback_gateway")
	except Exception as e:
		logger.error(e)
		request.session["status"] = False
		return redirect("callback_gateway")


def vandar_payment_verify(request):
	online_paid_amount = request.session.get("amount_payable")
	payment_purpose = request.session.get("payment_purpose")
	payment_token = request.session.get("token")

	try:
		verify_endpoint = "https://ipg.vandar.io/api/v3/verify"
		payload = json.dumps({
			"api_key": f'{api_token}',
			"token": payment_token
		})
		headers = {
			'Accept': 'application/json',
			'Content-Type': 'application/json',
			'Authorization': f'Bearer {access_token}',
		}
		response = requests.request(
			"POST", verify_endpoint, headers=headers, data=payload)
		payment_status = response.json()["status"]
		payment_message = response.json()["message"]
		if payment_status == 1 or payment_status == 0:
			if payment_message == "ok":
				user = request.user
				if payment_purpose == "pay_order_online":
					if online_paid_amount < 1000:
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
										 payment_gateway=_('Vandar'),
										 ip=request.META.get('REMOTE_ADDR'))
					request.session["status"] = True
					return redirect('callback_gateway')
				else:
					context = {"payment_purpose": "error"}
					return render(request, "accounts/callback_gateway.html", context)
	except Exception as e:
		logger.error(e)
		request.session["status"] = False
		return redirect("callback_gateway")
	return redirect("callback_gateway")
