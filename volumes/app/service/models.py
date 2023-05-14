from django.db import models
from django.utils.translation import gettext as _
import json

class ServiceType(models.Model):
    name = models.CharField(_('ServiceType'), max_length=100, blank=True, null=True)
    priority = models.IntegerField(_('Display priority'), blank=True, null=True)

    class Meta:
        ordering = ('id',)
        verbose_name = _('ServiceType')
        verbose_name_plural = _('ServiceTypes')

    def __str__(self) -> str:
        return f'{self.name}'


LINK_TYPE_CHOICES = (
    ("instagram_profile", "Instagram Profile(ID)"),
    ("instagram_post_link", "Instagram Post Link"),
)

SERVER = (
    ("parsifollower", "Parsifollower"),
    ("mifa", "Mifa"),
)

class Service(models.Model):
    service_type = models.ForeignKey(ServiceType, verbose_name=_('ServiceType'), on_delete=models.DO_NOTHING)
    link_type = models.CharField(max_length=20, choices=LINK_TYPE_CHOICES, verbose_name=_('Link Type'))
    server = models.CharField(max_length=20, choices=SERVER, verbose_name=_('Server'))
    server_service_code = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('Server Service Code'))
    service_code = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('Service Code'))
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Title'))
    amount = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('Amount Per 1 Number'))
    min_order = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('Min Order'))
    max_order = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('Max Order'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    priority = models.IntegerField(_('Display priority'), blank=True, null=True)
    available_for_user = models.BooleanField(default=True, verbose_name=_('Available For User'))

    def __str__(self) -> str:
        return f'{self.title}'

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def save(self, *args, **kwargs):
        pkgs = {}
        self.service_code = self.id
        factor = [1,2,3,4,5,10,20,30,50,100]
        for index, item in enumerate(factor):
            temp_dict = {}
            quantity = int(self.min_order) * int(item)
            temp_dict["quantity"] = quantity
            temp_dict["total_price"] = int(quantity) * int(self.amount)
            pkgs[index] = temp_dict
        pkgs = json.dumps(pkgs)
        self.template_packages = json.loads(pkgs)
        super(Service, self).save(*args, **kwargs)
