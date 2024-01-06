from celery import shared_task
from accounts.models import User
from common.send_sms import (
    send_login_sms,
    send_increase_credit_sms,
    send_register_sms,
    send_register_success_sms
)
import datetime
import time


@shared_task()
def send_login_sms_task(phone_number, verification_code):
    try:
        send_login_sms(phone_number, verification_code)
    except ValueError as exp:
        print("Error", exp)
    return "Ok!"


@shared_task()
def send_increase_credit_task(phone_number, amount, credit):
    try:
        send_increase_credit_sms(phone_number, amount, credit)
    except ValueError as exp:
        print("Error", exp)

    return "Ok!"


@shared_task()
def send_register_sms_task(phone_number, verification_code):
    try:
        send_register_sms(phone_number, verification_code)
    except ValueError as exp:
        print("Error", exp)

    return "Ok!"


@shared_task()
def send_register_success_sms_task(phone_number):
    now = datetime.datetime.now()
    time = now.strftime("%H:%M")
    try:
        send_register_success_sms(phone_number, time)
    except ValueError as exp:
        print("Error", exp)

    return "Ok!"


@shared_task()
def submit_order_count():
    users = User.objects.all()
    for user in users:
        orders_count = user.orders.all().count()
        user.orders_count = orders_count
        user.save()
        time.sleep(0.0000001)
    
    return "OK"