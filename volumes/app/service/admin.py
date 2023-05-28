from django.contrib import admin
from .models import Service, ServiceType
from django.utils.translation import gettext as _


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'priority', 'id']



@admin.action(description=_('به روز رسانی سرویس ها'))
def update_services(modeladmin, request, queryset):
    for obj in queryset:
        obj.save()


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price_1000_site', 'price_1000_server' , 'priority', 'server_service_code', 'server', 'service_type', 'available_for_user']
    actions = [update_services]
