from django.db import models
from django.utils.translation import gettext_lazy as _

class Setting(models.Model):
    auto_orders_submission = models.BooleanField(verbose_name=_("Automatic Orders Submission"), null=True, blank=True, default=True)
    max_amount_auto_submit = models.IntegerField(verbose_name=_("Max Amount Auto Submit"), null=True, blank=True)

    class Meta:
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")

    def __str__(self) -> str:
        return f'{self.auto_orders_submission}'