from celery import shared_task
from common.send_sms import (
    send_login_sms,
    send_increase_credit_sms,
    send_register_sms,
    send_register_success_sms
)
from accounts.models import User
import json
from django.conf import settings
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
def import_users_task():
    # for user in User.objects.all():
    #     if not user.phone_number == "09302521022":
    #         user.delete()
    # for user in User.objects.all():
    #     if user.email is None:
    #         user.email = f'{user.phone_number}@iranigram.com'
    #         user.save()
    filepath = settings.BASE_DIR / 'utils/files/total_users_file.json'
    with open(filepath, 'r') as f:
        users_data = f.read()
    users_data = json.loads(users_data)
    users_dict = {}
    for i, user in enumerate(users_data):
        users_dict[i] = user
        if not User.objects.filter(
            phone_number=user["phone_number"]
            ).exists() and len(user["phone_number"]) == 11 and not user["phone_number"].startswith("8"):
            User.objects.update_or_create(
                phone_number=user["phone_number"],
                email=user["email"],
                full_name=user["full_name"],
                amount_change_wallet=0,
                status_change_wallet="do_nothing",
                description_change_wallet="",
                is_block=user["is_block"],
                is_active=user["is_active"],
                balance=user["balance"],
                )
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