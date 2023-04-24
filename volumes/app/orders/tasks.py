from celery import shared_task
from utils.servers.parsifollower import PFOrderManager
from utils.servers.mifa import MifaOrderManager
from orders.models import Order
import json
from django.db.models import Q
import logging
from transactions.models import Transactions
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from utils.utils import get_jdatetime
from django.http import HttpResponse
from django.conf import settings
import time

logger = logging.getLogger("orders.tasks.order_status_task")


@shared_task()
def submit_order_task():
    orders = Order.objects.filter(status='Queued', paid=True)
    for order in orders:
        order_id = order.id
        order_server = order.service.server
        if order_server == "parsifollower":
            try:
                order_manager = PFOrderManager(order_id)
                response = order_manager.submit_order()
                r = json.loads(response.decode('utf-8'))
                logger.info("Order submitted in Parsifollower Server")
                if r['status'] == "success":
                    order.status = "Pending"
                    order.server_order_code = r["order"]
                    order.save()
            except ValueError as exp:
                logger.error(exp)
        elif order_server == "mifa":
            try:
                order_manager = MifaOrderManager(order_id)
                response = order_manager.submit_order()
                logger.info("Order submitted in Mifa Server")
                r = json.loads(response)
                if r['order']:
                    order.status = "Pending"
                    order.server_order_code = r["order"]
                    order.save()
            except ValueError as exp:
                logger.error(exp)
    return "Ok!"


@shared_task()
def order_status_task():
    orders = Order.objects.filter(
        Q(status='Pending') |
        Q(status='Processing') |
        Q(status='In progress') |
        Q(status='Canceled') |
        Q(status='Completed') |
        Q(status='Partial') |
        Q(status='Refunded'))
    for order in orders:
        if order.status not in ["Canceled", "Completed", "Partial", "Refunded"]:
            order_id = order.id
            order_server = order.service.server
            if order_server == "parsifollower":
                try:
                    order_manager = PFOrderManager(order_id)
                    response = order_manager.order_status()
                    logger.info("Get order status from Parsifollower server")
                    r = json.loads(response.decode('utf-8'))
                    if r["status"]:
                        order.status = r["status"]
                        if r["status"] == 'Canceled':
                            if User.objects.filter(phone_number=order.user.phone_number).exists():
                                user = User.objects.filter(phone_number=order.user.phone_number).first()
                                user.balance += order.amount
                                user.save()
                            Transactions.objects.create(
                                user=order.user,
                                type="return_canceled_order_fee",
                                price=order.amount,
                                balance=order.user.balance,
                                payment_type=order.payment_method,
                                details=_("Canceled"),
                                order_code=order.order_code,
                                payment_gateway=_('Zarinpal'))
                    if r["start_count"]:
                        order.start_count = r["start_count"]
                    if r["remains"]:
                        order.remains = r["remains"]
                    order.save()
                except ValueError as exp:
                    logger.error(exp)
            elif order_server == "mifa":
                try:
                    order_manager = MifaOrderManager(order_id)
                    response = order_manager.order_status()
                    logger.info("Get order status from Mifa server")
                    r = json.loads(response)
                    if r["status"]:
                        order.status = r["status"]
                        if r["status"] == 'Canceled':
                            if User.objects.filter(phone_number=order.user.phone_number).exists():
                                user = User.objects.filter(phone_number=order.user.phone_number).first()
                                user.balance += order.amount
                                user.save()
                            Transactions.objects.create(
                                user=order.user,
                                type="return_canceled_order_fee",
                                price=order.amount,
                                balance=order.user.balance,
                                payment_type=order.payment_method,
                                details=_("Canceled"),
                                order_code=order.order_code,
                                payment_gateway=_('Zarinpal'))
                    if r["start_count"]:
                        order.start_count = r["start_count"]
                    if r["remains"]:
                        order.remains = r["remains"]
                    order.save()
                except ValueError as exp:
                    logger.error(exp)
    return "Ok!"


@shared_task()
def import_orders_task():
    # count = 0
    # for order in Order.objects.all():
    #     order.delete()
    #     count += 1
    #     print(count)
    filepath = settings.BASE_DIR / 'utils/total_orders_file.json'
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
        time.sleep(0.1)
    return HttpResponse("ok")