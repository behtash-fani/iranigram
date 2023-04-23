from django.http import HttpResponse
from accounts.models import User
from orders.models import Order
import json
import os
from django.conf import settings
from celery import shared_task




@shared_task()
def import_users_task():
    # for user in User.objects.all():
    #     if user.email is None:
    #         user.email = f'{user.phone_number}@iranigram.com'
    #         user.save()
    filepath = settings.BASE_DIR / 'utils/total_users_file.json'
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


# def import_orders(request):
    # count = 0
    # for order in Order.objects.all():
    #     order.delete()
    #     count += 1
    #     print(count)
    # ======================
    # count = 0
    # filepath = settings.BASE_DIR / 'utils/total_orders_file.json'
    # with open(filepath, 'r') as f:
    #     orders_data = f.read()
    # orders_data = json.loads(orders_data)
    # orders_dict = {}
    # for i, order in enumerate(orders_data):
    #     orders_dict[i] = order
    #     # if not Order.objects.filter(order_code=order["order_code"]).exists():
    #     if User.objects.filter(phone_number=order["user"]).exists():
    #         user = User.objects.get(phone_number=order["user"])
    #     Order.objects.update_or_create(
    #         user=user,
    #         order_code=order["order_code"],
    #         link=order["link"],
    #         quantity=order["quantity"],
    #         amount=order["amount"],
    #         status=order["status"],
    #         payment_method=order["payment_method"],
    #         paid=order["paid"],
    #         )
    #     count += 1
    #     print(count)
    # return HttpResponse("ok")