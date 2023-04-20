from celery import shared_task
from utils.servers.parsifollower import PFOrderManager
from utils.servers.mifa import MifaOrderManager
from orders.models import Order
import json
from django.db.models import Q


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
                if r['status'] == "success":
                    order.status = "Pending"
                    order.server_order_code = r["order"]
                    order.save()
            except ValueError as exp:
                print("Error", exp)
        elif order_server == "mifa":
            try:
                order_manager = MifaOrderManager(order_id)
                response = order_manager.submit_order()
                r = json.loads(response)
                if r['order']:
                    order.status = "Pending"
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
            order_id = order.id
            order_server = order.service.server
            if order_server == "parsifollower":
                try:
                    order_manager = PFOrderManager(order_id)
                    response = order_manager.order_status()
                    r = json.loads(response.decode('utf-8'))
                    if r["status"]:
                        order.status = r["status"]
                    if r["start_count"]:
                        order.start_count = r["start_count"]
                    if r["remains"]:
                        order.remains = r["remains"]
                    order.save()
                except ValueError as exp:
                    print("Error", exp)
            elif order_server == "mifa":
                try:
                    order_manager = MifaOrderManager(order_id)
                    response = order_manager.order_status()
                    print(response)
                    r = json.loads(response)
                    if r["status"]:
                        order.status = r["status"]
                    if r["start_count"]:
                        order.start_count = r["start_count"]
                    if r["remains"]:
                        order.remains = r["remains"]
                    order.save()
                except ValueError as exp:
                    print("Error", exp)

