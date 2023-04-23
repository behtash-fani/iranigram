from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_code', 'user', 'status', 'server_order_code', 'amount','paid', 'payment_method', 'service',
                    'created_at']
    list_display_links = ('id', 'order_code', 'user')
    search_fields = ('user__phone_number__icontains','order_code')
    autocomplete_fields = ['user']
