from django.contrib import admin
from .models import Service, ServiceType, Packages
from django.utils.translation import gettext as _


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "priority", "id"]


@admin.action(description=_("به روز رسانی سرویس ها"))
def update_services(modeladmin, request, queryset):
    for obj in queryset:
        obj.save()


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "price_1000_site",
        "price_1000_server",
        "service_code",
        "priority",
        "server_service_code",
        "server",
        "service_type",
        "available_for_user",
        "available_for_package",
    ]
    list_display_links = ["id", "title"]
    actions = [update_services]


@admin.register(Packages)
class PackagesAdmin(admin.ModelAdmin):
    list_display = ["id", "service", "quantity", 'amount', 'priority', 'enable']
    list_display_links = ["id", "service", 'priority']
