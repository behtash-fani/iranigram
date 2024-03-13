from django.contrib import admin
from .models import NotificationCategory, Notification
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import datetime2jalali
from django.utils.html import format_html

class NotificationCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    search_fields = ('title', 'slug',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notice_category', 'is_active', 'get_created_jalali', 'get_updated_jalali',)
    list_filter = ('category', 'created_at', 'updated_at', )
    search_fields = ('title', 'detail', 'category__title',)
    autocomplete_fields = ["readers"]
    
    @admin.display(description="تاریخ ایجاد", ordering="created_at")
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime("%Y/%m/%d - %H:%M")
    
    @admin.display(description="تاریخ به روزرسانی", ordering="updated_at")
    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated_at).strftime("%Y/%m/%d - %H:%M")
    
    def notice_category(self, obj):
        return format_html('<a href="/igadmini/notification/notificationcategory/%s/change/">دسته بندی</a>' % obj.category.id)
    
    notice_category.short_description = 'دسته بندی'

admin.site.register(NotificationCategory, NotificationCategoryAdmin)
admin.site.register(Notification, NotificationAdmin)
