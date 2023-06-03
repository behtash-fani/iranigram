from django.contrib import admin
from .models import Transactions
from jalali_date import datetime2jalali
from django.urls import reverse
from django.utils.html import format_html
from orders.models import Order



@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['user', 'type','order_code_link', 'payment_type', 'price', 'balance', 'get_created_jalali']
    autocomplete_fields = ['user']


    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')
    
    def order_code_link(self, obj):
        order = Order.objects.get(order_code=obj.order_code)
        url = reverse("admin:orders_order_change", args=[order.id])
        return format_html("<a href='{}'>{}</a>", url, obj.order_code)

    order_code_link.short_description = "کد سفارش"
