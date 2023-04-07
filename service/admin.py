from django.contrib import admin
from .models import Service, ServiceType


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'server_service_code', 'server', 'service_type', 'available_for_user']
