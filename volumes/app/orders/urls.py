from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('pay-remain-price/', views.pay_remain_price, name='pay_remain_price'),
    path('complete-order-payment/', views.complete_order, name='complete_order'),
    ]
