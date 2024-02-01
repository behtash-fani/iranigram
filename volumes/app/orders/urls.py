from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('complete-order-payment/', views.complete_order, name='complete_order'),
    path('<str:pkg_id>/new-order/', views.TemplateNewOrder.as_view(), name='new_order'),
    path('get-insta-info/', views.get_insta_info, name='get_insta_info'),
    path('get-phone-number/', views.get_phone_number, name='get_phone_number'),
    path('verify-phonenumber-pay/', views.verify_phonenumber_pay, name='verify_phonenumber_pay'),
    path('to-gateways/', views.send_to_payment, name='send_to_payment'),
    ]
