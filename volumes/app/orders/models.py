from django.db import models
from accounts.models import User
from service.models import Service, ServiceType
from django.utils.translation import gettext_lazy as _

ORDER_STATUS = (
    ("Queued", _("Queued")),  # در حال ثبت سفارش
    ("Pending", _('Pending')),  # در دست انجام
    ("Processing", _("Processing")),  # در حال پردازش
    ("In progress", _("In progress")),  # در حال انجام
    ("Canceled", _("Canceled")),  # لغو شده
    ("Completed", _("Completed")),  # کامل شده
    ("Partial", _("Partial")),  # ناتمام
    ("Refunded", _("Refunded")),  # برگشت مبلغ شده
)

PAYMENT_METHOD = (
    ("online", _("online")),
    ("wallet", _("Wallet")),
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name=_('User'), related_name='orders')
    service_type = models.ForeignKey(ServiceType,on_delete=models.DO_NOTHING,blank=True, null=True,verbose_name=_('ServiceType'))
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, blank=True, null=True,verbose_name=_('Service'))
    server_order_code = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Server Order Code'))
    order_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Order Code'))
    link = models.CharField(max_length=1000, verbose_name=_('Link'), blank=True, null=True,)
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'), blank=True, null=True,)
    amount = models.PositiveIntegerField(default=0, verbose_name=_('Amount'))
    wallet_paid_amount = models.PositiveIntegerField(verbose_name=_('Wallet Paid Amount'), blank=True, null=True)
    online_paid_amount = models.PositiveIntegerField(verbose_name=_('Online Paid Amount'), blank=True, null=True)
    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHOD, verbose_name=_('Payment Method'), blank=True, null=True)
    status = models.CharField(max_length=30, choices=ORDER_STATUS,default="Queued", blank=True,null=True, verbose_name=_('Status'))
    start_count = models.PositiveIntegerField(verbose_name=_('Start Count'), blank=True, null=True)
    remains = models.PositiveIntegerField(verbose_name=_('Remains'), blank=True, null=True)
    paid = models.BooleanField(default=False, verbose_name=_('Paid'))
    submit_now = models.BooleanField(default=False, verbose_name=_("Submit Now"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class QueuedOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING,blank=True, null=True,verbose_name=_('Order'))

    def __str__(self):
        return f'{self.order.order_code}'

    class Meta:
        verbose_name = _('Queued Order')
        verbose_name_plural = _('Queued Orders')