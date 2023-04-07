from celery import shared_task
from utils.send_sms import (
    send_verification_sms,
    send_increase_credit_sms,
    send_register_sms,
    send_register_success_sms
)
from utils.utils import get_jdatetime


@shared_task()
def send_verification_sms_task(phone_number, verification_code):
    try:
        send_verification_sms(phone_number, verification_code)
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
    time = get_jdatetime()[1]  # index of 1 in jdatetime return persian time
    try:
        send_register_success_sms(phone_number, time)
    except ValueError as exp:
        print("Error", exp)

    return "Ok!"
