from django.contrib import admin
from .models import Order, QueuedOrder
from django.urls import reverse
from django.utils.html import format_html
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin
from django.db.models import Q
from django.contrib import messages
from transactions.models import Transactions as Trans
from django.utils.translation import gettext_lazy as _


@admin.action(description="تغییر وضعیت به کامل شده")
def make_complete_order(modeladmin, request, queryset):
    queryset.update(status="Completed")

@admin.action(description="الان ثبت شود")
def enable_submit_now(modeladmin, request, queryset):
    queryset.update(submit_now=True)

@admin.action(description="لغو سفارش")
def cancel_order(modeladmin, request, queryset):
    queryset.update(status="Canceled")
    for order in queryset:
        order.user.balance += order.amount
        order.user.save()
        Trans.objects.create(
                user=order.user,
                type="return_canceled_order_fee",
                price=order.amount,
                balance=order.user.balance,
                details=_("Canceled"),
                order_code=order.order_code,
                payment_gateway=_('Zarinpal'),
                ip=request.META.get('REMOTE_ADDR'),
            )


@admin.register(Order)
class OrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        "id",
        "order_code",
        "user_link",
        "quantity",
        "status",
        "server_order_code",
        "amount",
        "paid",
        "payment_method",
        "service",
        "get_created_jalali",
    ]
    list_display_links = ("id", "order_code", "user_link")
    search_fields = ("user__phone_number__icontains", "order_code", "link__icontains", "server_order_code",)
    autocomplete_fields = ["user"]
    actions = [make_complete_order, enable_submit_now, cancel_order]

    def user_link(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html("<a href='{}'>{}</a>", url, obj.user)

    user_link.short_description = "خریدار"

    @admin.display(description="تاریخ ایجاد", ordering="created_at")
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime("%Y/%m/%d - %H:%M")


@admin.register(QueuedOrder)
class QueuedOrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        "order_id",
        "order_code_link",
        "user_link",
        "amount",
        "status",
        "get_created_jalali",
    ]
    list_display_links = (
        "order_id",
        "order_code_link",
    )
    search_fields = ("order_code_link", "user_link")
    actions = [make_complete_order, enable_submit_now, cancel_order]

    # autocomplete_fields = ['user']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = Order.objects.filter(paid=True, status="Queued")
        return qs

    def order_id(self, obj):
        url = reverse("admin:orders_order_change", args=[obj.id])
        return format_html("<a href='{}'>{}</a>", url, obj)

    order_id.short_description = "آی دی سفارش"

    def order_code_link(self, obj):
        url = reverse("admin:orders_order_change", args=[obj.id])
        return format_html("<a href='{}'>{}</a>", url, obj.order_code)

    order_code_link.short_description = "کد سفارش"

    def amount(self, obj):
        return obj.amount

    amount.short_description = "قیمت نهایی قابل پرداخت"

    def status(self, obj):
        return obj.status

    status.short_description = "وضعیت"

    def service(self, obj):
        return obj.amount

    service.short_description = "سرویس"

    def user_link(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html("<a href='{}'>{}</a>", url, obj.user)

    user_link.short_description = "خریدار"

    @admin.display(description="تاریخ ایجاد", ordering="created_at")
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime("%Y/%m/%d - %H:%M")
