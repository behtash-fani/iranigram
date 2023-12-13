from django.contrib import admin
from .models import Comment, Response
from django.utils.translation import gettext as _
from django.urls import reverse
from django.utils.html import format_html
from jalali_date import datetime2jalali


class ResponseInline(admin.TabularInline):
    model = Response
    extra = 0


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    inlines = [ResponseInline]
    list_display = ('id', 'phone_number', 'content', 'status', 'page_id',
                    'response_count', 'get_created_jalali', 'get_updated_jalali')
    list_display_links = ('id', 'phone_number', 'content')

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='تاریخ به روزرسانی', ordering='updated_at')
    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated_at).strftime('%Y/%m/%d - %H:%M')

    def response_count(self, obj):
        return obj.response_set.count()

    response_count.short_description = _('Responses')

    def view_ticket_responses(self, obj):
        responses = obj.response_set.all()
        response_links = [
            f'<a href="{reverse("admin:support_tickets_response_change", args=[response.id])}">{response}</a>' for
            response in responses]
        return format_html('<br>'.join(response_links))

    view_ticket_responses.short_description = _('Responses')
