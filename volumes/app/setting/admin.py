from django.contrib import admin
from .models import Setting


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'id','active_payment_gateway',
                    'auto_orders_submission',  'max_amount_auto_submit']

