from django.contrib import admin
from .models import Transactions


@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'payment_type', 'price', 'balance', 'created_at']
    autocomplete_fields = ['user']
