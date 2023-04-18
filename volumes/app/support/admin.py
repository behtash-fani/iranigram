from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Ticket, Response
from django.utils.translation import gettext as _


class ResponseInline(admin.TabularInline):
    model = Response
    extra = 0


class TicketAdmin(admin.ModelAdmin):
    inlines = [ResponseInline]
    list_display = ('id', 'subject', 'user', 'status', 'created_at', 'updated_at', 'response_count')
    list_display_links = ('id', 'subject', 'user')
    readonly_fields = ('created_at', 'updated_at')
    fields = ('user', 'subject', 'message', 'file', 'status', 'created_at', 'updated_at')
    ordering = ('-created_at',)

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

    # def get_fieldsets(self, request, obj=None):
    #     fieldsets = super().get_fieldsets(request, obj=obj)
    #     if obj is not None:
    #         fieldsets += (('Responses', {'fields': ('view_ticket_responses',)}),)
    #     return fieldsets


admin.site.register(Ticket, TicketAdmin)
# admin.site.register(Response)
