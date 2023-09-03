from celery import shared_task
from common.servers.parsifollower import Parsifollower
from common.servers.berlia import Berlia
from orders.models import Order
from django.db.models import Q
from transactions.models import Transactions
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from django.conf import settings
from common.send_sms import send_submit_order_sms, send_cancel_order_sms


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
    orders = Order.objects.filter(status="Queued", paid=True)
    for order in orders:
        if settings.SUBMIT_AUTOMATIC_ORDERS == True or order.submit_now == True:
            if order.service is not None:
                order_id = order.id
                order = Order.objects.get(id=order_id)
                service = order.service.server_service_code
                link = order.link
                quantity = order.quantity
                order_server = order.service.server
                if order_server == "parsifollower":
                    try:
                        order_manager = Parsifollower()
                        submitted_order = order_manager.submit_order(
                            service, link, quantity
                        )
                        if "order" in submitted_order:
                            order.status = "Pending"
                            order.server_order_code = submitted_order["order"]
                            order.save()
                    except ValueError as exp:
                        print(exp)
                elif order_server == "berlia":
                    try:
                        order_manager = Berlia()
                        submitted_order = order_manager.submit_order(
                            service, link, quantity
                        )
                        if "order" in submitted_order:
                            order.status = "Pending"
                            order.server_order_code = submitted_order["order"]
                            order.save()
                    except ValueError as exp:
                        print(exp)
                pass
    return "Ok!"


@shared_task()
def order_status_task():
    orders = Order.objects.filter(
        Q(status="Pending") | Q(status="Processing") | Q(status="In progress")
    ).exclude(service__isnull=True)
    for order in orders:
        order_id = order.id
        order = Order.objects.get(id=order_id)
        server_order_code = order.server_order_code
        order_server = order.service.server
        if order_server == "parsifollower":
            try:
                order_manager = Parsifollower()
                order_status = order_manager.order_status(server_order_code)
                if "status" in order_status:
                    order.status = order_status["status"]
                    if order_status["status"] == "Canceled":
                        if User.objects.filter(
                            phone_number=order.user.phone_number
                        ).exists():
                            user = User.objects.filter(
                                phone_number=order.user.phone_number
                            ).first()
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
                                payment_gateway=_("Zarinpal"),
                            )
                            send_cancel_order_sms_task.delay(
                                order.user.phone_number, order.order_code
                            )
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
                order_manager = Berlia()
                order_status = order_manager.order_status(server_order_code)
                if "status" in order_status:
                    order.status = order_status["status"]
                    if order_status["status"] == "Canceled":
                        if User.objects.filter(
                            phone_number=order.user.phone_number
                        ).exists():
                            user = User.objects.filter(
                                phone_number=order.user.phone_number
                            ).first()
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
                                payment_gateway=_("Zarinpal"),
                            )
                            send_cancel_order_sms_task.delay(
                                order.user.phone_number, order.order_code
                            )
                    if "start_count" in order_status:
                        order.start_count = order_status["start_count"]
                    if "remains" in order_status:
                        order.remains = order_status["remains"]
                    order.save()
            except ValueError as exp:
                print(exp)
    return "Ok!"
