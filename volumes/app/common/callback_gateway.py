from django.shortcuts import render
from accounts.models import User
from orders.models import Order


def callback_gateway(request):
    phone = request.session["phone_number"]
    user = User.objects.get(phone_number=phone)
    user_balance = user.balance
    payment_type = request.session["payment_type"]
    if request.session['status']:
        if request.session['payment_type'] == 'add_fund_wallet':
            context = {'payment_type': payment_type, 'user_balance': user_balance}
            return render(request, 'accounts/callback_gateway.html', context)
        elif request.session['payment_type'] == 'pay_order_online':
            order_id = request.session['order_id']
            order_code = Order.objects.get(id=order_id).order_code
            context = {'payment_type': payment_type, 'order_code': order_code}
            return render(request, 'accounts/callback_gateway.html', context)
        elif request.session['payment_type'] == 'pay_remain_price':
            order_id = request.session['order_id']
            order_code = Order.objects.get(id=order_id).order_code
            context = {'payment_type': payment_type, 'order_code': order_code}
            return render(request, 'accounts/callback_gateway.html', context)
    else:
        context = {'payment_type': 'error'}
        return render(request, 'accounts/callback_gateway.html', context)
