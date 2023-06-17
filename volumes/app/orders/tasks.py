from celery import shared_task
from common.servers.parsifollower import PFOrderManager
from common.servers.berlia import BLOrderManager
from common.servers.mifa import MifaOrderManager
from orders.models import Order
import json
from django.db.models import Q
from transactions.models import Transactions
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from django.http import HttpResponse
from django.conf import settings
from common.send_sms import (
    send_submit_order_sms,
    send_cancel_order_sms
)




@shared_task()
def send_submit_order_sms_task(phone_number, order_code):
    try:
        send_submit_order_sms(phone_number, order_code)
    except ValueError as exp:
        print("Error", exp)
      
@shared_task()
def send_cancel_order_sms_task(phone_number, order_code):
    try:
        send_cancel_order_sms(phone_number, order_code)
    except ValueError as exp:
        print("Error", exp)


@shared_task()
def submit_order_task():
    orders = Order.objects.filter(status='Queued', paid=True)
    for order in orders:
        if settings.SUBMIT_AUTOMATIC_ORDERS == True or order.submit_now == True:
            if order.service is not None:
                order_id = order.id
                order_server = order.service.server
                if order_server == "parsifollower":
                    try:
                        order_manager = PFOrderManager(order_id)
                        response = order_manager.submit_order()
                        r = json.loads(response.decode('utf-8'))
                        if "order" in r:
                            order.status = "Pending"
                            order.server_order_code = r["order"]
                            order.save()
                    except ValueError as exp:
                        print(exp)
                elif order_server == "berlia":
                    try:
                        order_manager = BLOrderManager(order_id)
                        response = order_manager.submit_order()
                        r = json.loads(response.decode('utf-8'))
                        if "order" in r:
                            order.status = "Pending"
                            order.server_order_code = r["order"]
                            order.save()
                    except ValueError as exp:
                        print(exp)
                elif order_server == "mifa":
                    try:
                        order_manager = MifaOrderManager(order_id)
                        response = order_manager.submit_order()
                        r = json.loads(response)
                        if 'order' in r:
                            order.status = "Pending"
                            order.server_order_code = r["order"]
                            order.save()
                    except ValueError as exp:
                        print(exp)
            else:
                pass
    return "Ok!"


@shared_task()
def order_status_task():
    orders = Order.objects.filter(Q(status='Pending') | Q(status='Processing') | Q(status='In progress')).exclude(service__isnull=True)
    for order in orders:
        order_id = order.id
        for order_server in ["parsifollower", "berlia"]:
            if order_server == "parsifollower":
                try:
                    order_manager = PFOrderManager(order_id)
                    response = order_manager.order_status()
                    order_status = json.loads(response.decode('utf-8'))
                    if "status" in order_status:
                        order.status = order_status["status"]
                        if order_status["status"] == 'Canceled':
                            if User.objects.filter(phone_number=order.user.phone_number).exists():
                                user = User.objects.filter(phone_number=order.user.phone_number).first()
                                user.balance += order.amount
                                user.save()
                                order.status = "Canceled"
                                order.save()
                                Transactions.objects.create(
                                    user=order.user,
                                    type="return_canceled_order_fee",
                                    price=order.amount,
                                    balance=order.user.balance,
                                    payment_type=order.payment_method,
                                    details=_("Canceled"),
                                    order_code=order.order_code,
                                    payment_gateway=_('Zarinpal'))
                                send_cancel_order_sms_task.delay(order.user.phone_number, order.order_code)
                        if order_status["start_count"]:
                            order.start_count = order_status["start_count"]
                        if order_status["remains"]:
                            order.remains = order_status["remains"]
                        order.save()
                    elif "error" in order_status:
                        continue
                except ValueError as exp:
                    print(exp)
            elif order_server == "berlia":
                try:
                    order_manager = BLOrderManager(order_id)
                    response = order_manager.order_status()
                    order_status = json.loads(response.decode('utf-8'))
                    if "status" in order_status:
                        order.status = order_status["status"]
                        if order_status["status"] == 'Canceled':
                            if User.objects.filter(phone_number=order.user.phone_number).exists():
                                user = User.objects.filter(phone_number=order.user.phone_number).first()
                                user.balance += order.amount
                                user.save()
                                order.status = "Canceled"
                                order.save()
                                Transactions.objects.create(
                                    user=order.user,
                                    type="return_canceled_order_fee",
                                    price=order.amount,
                                    balance=order.user.balance,
                                    payment_type=order.payment_method,
                                    details=_("Canceled"),
                                    order_code=order.order_code,
                                    payment_gateway=_('Zarinpal'))
                                send_cancel_order_sms_task.delay(order.user.phone_number, order.order_code)
                        if "start_count" in order_status:
                            order.start_count = order_status["start_count"]
                        if "remains" in order_status:
                            order.remains = order_status["remains"]
                        order.save()
                except ValueError as exp:
                    print(exp)
    return "Ok!"


@shared_task()
def import_orders_task():
    count = 0
    # for order in Order.objects.all():
    #     if order.status == "Queued":
    #         order.status = "Pending"
    #         order.save()
    #     count += 1
    #     print(count)
    filepath = settings.BASE_DIR / 'utils/files/total_orders_file.json'
    with open(filepath, 'r') as f:
        orders_data = f.read()
    orders_data = json.loads(orders_data)
    orders_dict = {}
    for i, order in enumerate(orders_data):
        orders_dict[i] = order
        # if not Order.objects.filter(order_code=order["order_code"]).exists():
        if User.objects.filter(phone_number=order["user"]).exists():
            user = User.objects.get(phone_number=order["user"])
        Order.objects.update_or_create(
            user=user,
            order_code=order["order_code"],
            link=order["link"],
            quantity=order["quantity"],
            amount=order["amount"],
            status=order["status"],
            payment_method=order["payment_method"],
            paid=order["paid"],
            )
        # print(i)
    return HttpResponse("ok")





