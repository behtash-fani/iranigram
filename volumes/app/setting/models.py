from django.db import models
from django.utils.translation import gettext_lazy as _


PAYMENT_GATEWAYS = (
    ("zarinpal", _("Zarinpal")),
    ("vandar", _("Vandar")),
)


class Setting(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=255, null=True, blank=True)
    auto_orders_submission = models.BooleanField(verbose_name=_("Automatic Orders Submission"), null=True, blank=True, default=True)
    max_amount_auto_submit = models.IntegerField(verbose_name=_("Max Amount Auto Submit"), null=True, blank=True)
    active_payment_gateway = models.CharField(max_length=30, choices=PAYMENT_GATEWAYS, default="zarinpal", blank=True, null=True, verbose_name=_('Active Payment Gateway'))

    class Meta:
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")

    def __str__(self) -> str:
        return f'{self.auto_orders_submission}'
