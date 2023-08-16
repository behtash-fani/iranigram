from accounts.models import User




def submit_order_count(request):
    users = User.objects.all()
    for user in users:
        orders_count = user.orders.all().count()
        user.orders_count = orders_count
        user.save()
    
    return "OK"