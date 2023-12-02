from django.contrib import admin
from .models import Post,Category
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','get_created_jalali')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    autocomplete_fields = ['author']

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')


admin.site.register(Category)