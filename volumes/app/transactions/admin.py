from django.contrib import admin
from .models import Transactions
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin	



@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'payment_type', 'price', 'balance', 'get_created_jalali']
    autocomplete_fields = ['user']


    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')
