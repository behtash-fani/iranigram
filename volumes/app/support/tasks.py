from celery import shared_task
from common.send_sms import (
    send_submit_ticket_sms,
    send_support_answer_ticket_sms,
    send_user_answer_ticket_sms
)


@shared_task()
def send_submit_ticket_sms_task(phone_number, ticketCode):
    try:
        send_submit_ticket_sms(phone_number, ticketCode)
    except ValueError as exp:
        print("Error", exp)

    return "Ok!"


@shared_task()
def send_support_answer_ticket_sms_task(phone_number, ticketCode):
    try:
        send_support_answer_ticket_sms(phone_number, ticketCode)
    except ValueError as exp:
        print("Error", exp)

    return "Ok!"


@shared_task()
def send_user_answer_ticket_sms_task(phone_number, ticketCode):
    try:
        send_user_answer_ticket_sms(phone_number, ticketCode)
    except ValueError as exp:
        print("Error", exp)

    return "Ok!"
