from django.contrib import admin
from .models import Transactions
from jalali_date import datetime2jalali



@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['user', 'type','order_code', 'payment_type', 'price', 'balance', 'get_created_jalali']
    autocomplete_fields = ['user']
    search_fields = ('user__phone_number__icontains',)


    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')
