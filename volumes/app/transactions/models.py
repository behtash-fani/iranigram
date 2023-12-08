from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _

TYPE = (
    ("increase_ab_by_admin", _("increase_ab_by_admin")),  # افزایش شارژ دستی مدیر
    ("decrease_ab_by_admin", _('decrease_ab_by_admin')),  # کاهش شارژ دستی مدیر
    ("payment_for_order", _("payment_for_order")),  # هزینه سفارش
    ("add_fund", _("add_fund")),  # شارژ حساب
    ("return_canceled_order_fee", _("return_canceled_order_fee")),  # برگشت هزینه سفارش کنسلی
    ("return_partial_order_fee", _("return_partial_order_fee")),  # برگشت هزینه سفارش ناقص
)

PAYMENT_TYPE = (
    ("wallet", _("wallet")),
    ("online", _("online")),
    ("system", _("system")),
)


class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    type = models.CharField(max_length=30, choices=TYPE, blank=True, null=True, verbose_name=_('Type of transaction'))
    price = models.PositiveIntegerField(blank=True, verbose_name=_('Price'))
    balance = models.IntegerField(blank=True, null=True, verbose_name=_('Balance'))
    payment_type = models.CharField(max_length=300, choices=PAYMENT_TYPE, blank=True, null=True,
                                    verbose_name=_('Payment Type'), default='system')
    details = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Details'))
    order_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Order Code'))
    payment_gateway = models.CharField(max_length=30, blank=True, default=_('system'), verbose_name=_('Payment Gateway'))
    payment_ref = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Payment Ref'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    ip = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('IP'))

    def __str__(self) -> str:
        return f"{self.user}"

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
