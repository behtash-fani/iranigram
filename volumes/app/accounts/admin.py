from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User
from .models import OTPCode
from jalali_date.admin import ModelAdminJalaliMixin
from django.utils.translation import gettext_lazy as _
from transactions.models import Transactions as Trans
from jalali_date import datetime2jalali
from import_export.admin import ImportExportModelAdmin
from orders.models import Order
from django.db.models import Count

@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'expire_time' , 'get_created_jalali')

    @admin.display(description="تاریخ ایجاد", ordering="created_at")
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime("%Y/%m/%d - %H:%M")


class UserAdmin(ImportExportModelAdmin, ModelAdminJalaliMixin, BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('phone_number', 'full_name', 'balance','orders_count', 'is_block', 'is_active')
    list_filter = ('is_admin',)
    search_fields = ('phone_number__icontains', 'full_name__icontains', 'email__icontains')
    fieldsets = (
        (
            'personal information', {'fields': ('phone_number', 'full_name', 'email', 'password',)}
        ),
        (
            'Wallet',
            {'fields': ('balance', 'amount_change_wallet', 'status_change_wallet', 'description_change_wallet')}
        ),
        (
            'Activity', {'fields': ('orders_count',)}
        ),
        (
            'Permissions', {'fields': ('is_block', 'is_admin', 'is_active', 'last_login')}
        ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ()
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if obj.status_change_wallet == "add_credit":
            if obj.balance is None:
                obj.balance = 0
            obj.balance += obj.amount_change_wallet
            Trans.objects.create(
                user=request.user,
                type="increase_ab_by_admin",
                price=obj.amount_change_wallet,
                balance=obj.balance,
                details=obj.description_change_wallet,
                ip=request.META.get('REMOTE_ADDR'),
            )
        elif obj.status_change_wallet == "reduce_credit":
            obj.balance -= obj.amount_change_wallet
            Trans.objects.create(
                user=request.user,
                type="decrease_ab_by_admin",
                price=obj.amount_change_wallet,
                balance=obj.balance,
                details=obj.description_change_wallet,
                ip=request.META.get('REMOTE_ADDR'),
            )
        obj.amount_change_wallet = 0
        obj.status_change_wallet = "do_nothing"
        obj.description_change_wallet = ""
        super().save_model(request, obj, form, change)

    class Meta:
        localized_fields = '__all__'


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
