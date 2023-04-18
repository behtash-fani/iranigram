from celery import shared_task
from utils.parsifollower import OrderManager
from orders.models import Order
import json
from django.db.models import Q


@shared_task()
def submit_order_task():
    orders = Order.objects.filter(status='queued', paid=True)
    for order in orders:
        order_code = order.order_code
        try:
            submit = OrderManager(order_code)
            response = submit.submit_order()
            r = json.loads(response.decode('utf-8'))
            if r['status'] == "success":
                order.status = "pending"
                order.server_order_code = r["order"]
                order.save()
        except ValueError as exp:
            print("Error", exp)
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
            order_code = order.order_code
            try:
                get_status = OrderManager(order_code)
                response = get_status.order_status()
                r = json.loads(response.decode('utf-8'))
                print(r)
                if r["status"]:
                    order.status = r["status"]
                if r["start_count"]:
                    order.start_count = r["start_count"]
                if r["remains"]:
                    order.remains = r["remains"]
                order.save()
            except ValueError as exp:
                print("Error", exp)
