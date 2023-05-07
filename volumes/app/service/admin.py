from django.contrib import admin
from .models import Service, ServiceType
from django.utils.translation import gettext as _


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'priority', 'id']



@admin.action(description=_('Mark selected items as template service'))
def make_template_service(modeladmin, request, queryset):
    for obj in queryset:
        if obj.template_service:
            queryset.update(template_service=False)
        else:
            queryset.update(template_service=True)

    

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'priority', 'server_service_code', 'server', 'service_type', 'available_for_user', 'template_service']
    actions = [make_template_service]
