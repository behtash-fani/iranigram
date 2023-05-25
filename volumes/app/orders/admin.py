from django.contrib import admin
from .models import Order, QueuedOrder
from django.urls import reverse
from django.utils.html import format_html
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin
from django.db.models import Q
from django.contrib import messages




@admin.register(Order)
class OrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['id', 'order_code', 'user_link','quantity', 'status', 'server_order_code',
        'amount','paid', 'payment_method', 'service', 'get_created_jalali']
    list_display_links = ('id', 'order_code', 'user_link')
    search_fields = ('user__phone_number__icontains','order_code', 'link')
    autocomplete_fields = ['user']


    def user_link(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html("<a href='{}'>{}</a>", url, obj.user)
    user_link.short_description = 'خریدار'

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(QueuedOrder)
class QueuedOrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['order_id','order_code','user_link','amount', 'get_created_jalali']
    list_display_links = ('order_id','order_code',)
    search_fields = ('order_code', 'user_link')
    # autocomplete_fields = ['user']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = Order.objects.filter(paid=True, status="Queued")
        return qs


    def order_id(self, obj):
        return obj.id
    order_id.short_description = 'آی دی'
    
    def order_code(self, obj):
        return obj.order_code
    order_code.short_description = 'کد سفارش'
    
    def amount(self, obj):
        return obj.amount
    amount.short_description = 'قیمت نهایی قابل پرداخت'


    def service(self, obj):
        return obj.amount
    service.short_description = 'سرویس'

    def user_link(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html("<a href='{}'>{}</a>", url, obj.user)
    user_link.short_description = 'خریدار'

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')