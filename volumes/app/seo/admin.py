from django.contrib import admin
from .models import PagesSeo





@admin.register(PagesSeo)
class PagesSeoAdmin(admin.ModelAdmin):
    list_display = ['page', 'title_tag',]