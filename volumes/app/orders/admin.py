from django.contrib import admin
from .models import Order
from django.urls import reverse
from django.utils.html import format_html

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_code', 'user_link', 'status', 'server_order_code',
        'amount','paid', 'payment_method', 'service','created_at']
    list_display_links = ('id', 'order_code', 'user_link')
    search_fields = ('user__phone_number__icontains','order_code')
    autocomplete_fields = ['user']


    def user_link(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html("<a href='{}'>{}</a>", url, obj.user)
    user_link.short_description = 'User'