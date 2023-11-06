from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Ticket, Response
from django.utils.translation import gettext as _
from jalali_date import datetime2jalali
from orders.models import Order



class ResponseInline(admin.TabularInline):
    model = Response
    extra = 0
    autocomplete_fields = ['user']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    inlines = [ResponseInline]
    list_display = ('id', 'subject', 'user', 'status','order_link', 'get_created_jalali', 'get_updated_jalali', 'response_count')
    list_display_links = ('id', 'subject', 'user')
    search_fields = ('user__phone_number', 'message__icontains')
    readonly_fields = ('get_created_jalali', 'get_updated_jalali')
    fields = ('user', 'subject', 'message', 'file', 'status', 'get_created_jalali', 'get_updated_jalali')
    ordering = ('-created_at',)
    autocomplete_fields = ['user']


    def order_link(self, obj):
        return format_html('<a href="/admin/orders/order/?q=%s">سفارشات کاربر</a>' % obj.user.phone_number)

    order_link.short_description = 'سفارشات کاربر'

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
    

# @admin.register(Response)
# class ResponseAdmin(admin.ModelAdmin):
#     autocomplete_fields = ['user']
