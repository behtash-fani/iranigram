from django.urls import path
from .views import pay_remain_price

app_name = 'orders'
urlpatterns = [
    path('pay-remain-price/', pay_remain_price, name='pay_remain_price'),
    ]
