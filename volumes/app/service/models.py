from django.db import models
from django.utils.translation import gettext as _
from common.servers.parsifollower import Parsifollower
from common.servers.berlia import Berlia


class ServiceType(models.Model):
    name = models.CharField(
        _("ServiceType"), max_length=100, blank=True, null=True)
    priority = models.IntegerField(
        _("Display priority"), blank=True, null=True)

    class Meta:
        ordering = ("id",)
        verbose_name = _("ServiceType")
        verbose_name_plural = _("ServiceTypes")

    def __str__(self) -> str:
        return f"{self.name}"


LINK_TYPE_CHOICES = (
    ("instagram_profile", "Instagram Profile(ID)"),
    ("instagram_post_link", "Instagram Post Link"),
    ("telegram_link", "Telegram Link(ID)"),
)

SERVER = (
    ("parsifollower", "Parsifollower"),
    ("berlia", "Berlia"),
    ("mifa", "Mifa"),
)


class Service(models.Model):
    service_type = models.ForeignKey(ServiceType, verbose_name=_("Service Type"), on_delete=models.DO_NOTHING)
    link_type = models.CharField(max_length=20, choices=LINK_TYPE_CHOICES, verbose_name=_("Link Type"))
    server = models.CharField(max_length=20, choices=SERVER, verbose_name=_("Server"))
    server_service_code = models.CharField(max_length=10, null=True, blank=True, verbose_name=_("Server Service Code"))
    service_code = models.CharField(max_length=10, null=True, blank=True, verbose_name=_("Service Code"))
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("Title"))
    amount = models.CharField(max_length=10, null=True, blank=True, verbose_name=_("Amount Per 1 Number"))
    price_1000_site = models.CharField(max_length=10, null=True, blank=True, verbose_name=_("Price For 1000 Site"))
    price_1000_server = models.CharField(max_length=10, null=True, blank=True, verbose_name=_("Price For 1000 Server"))
    min_order = models.CharField(max_length=10, null=True, blank=True, verbose_name=_("Min Order"))
    max_order = models.CharField(max_length=10, null=True, blank=True, verbose_name=_("Max Order"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    priority = models.IntegerField(_("Display Priority"), blank=True, null=True)
    available_for_user = models.BooleanField(default=True, verbose_name=_("Available For User"))
    available_for_package = models.BooleanField(default=False, verbose_name=_("Available For Package"))
    service_tag = models.CharField(max_length=50, verbose_name=_("Service Tag Name"), blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def save(self, *args, **kwargs):
        if self.server == "parsifollower":
            order_manager = Parsifollower()
        elif self.server == "berlia":
            order_manager = Berlia()
        service_code = self.server_service_code
        service_data = order_manager.get_service_data(service_code)
        rate = int(float(service_data["rate"]))
        self.price_1000_server = rate
        self.price_1000_site = int(self.amount) * 1000
        # update pkgs amount
        pkgs = Packages.objects.filter(service=self)
        for pkg in pkgs:
            pkg.amount = int(self.amount)*int(pkg.quantity)
            pkg.save()
        super().save(*args, **kwargs)


class Packages(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, verbose_name=_("Service")
    )
    quantity = models.CharField(_("Quantity"), max_length=50)
    amount = models.CharField(
        max_length=10, null=True, blank=True, verbose_name=_("Amount")
    )
    priority = models.IntegerField(
        _("Display Priority"), blank=True, null=True)
    

    def __str__(self) -> str:
        return f"{self.service}"

    class Meta:
        verbose_name = _("Package")
        verbose_name_plural = _("Packages")
