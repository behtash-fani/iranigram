# from django.db import models
# from django.contrib.auth import get_user_model


# class Comment(models.Model):
#     user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
#     content = models.TextField(max_length= 500, null=True, blank=True)
#     page_url = models.URLField()
#     is_approved = models.BooleanField(default=False)
#     parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
#     reply = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f'{self.user}'


from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _


STATUS = (
    ("not approved", _("Not Approved")),
    ("approved", _("Approved")),
)


class Comment(models.Model):
    phone_number = models.CharField(max_length = 13, verbose_name=_('Phone Number'), blank=True, null=True)
    name = models.CharField(max_length = 100, verbose_name=_('Name'), blank=True, null=True)
    content = models.TextField(verbose_name=_('Content'), blank=True, null=True)
    page_id = models.CharField(verbose_name=_('Page ID'), max_length= 50, blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS, verbose_name=_('Status'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'), blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'), blank=True, null=True)

    def __str__(self):
        return f'{self.phone_number}'

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


class Response(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name=_('Comment'))
    phone_number = models.CharField(max_length = 13, verbose_name=_('Phone Number'), blank=True, null=True)
    content = models.TextField(verbose_name=_('Content'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'), blank=True, null=True)

    def __str__(self):
        return f'{self.comment.phone_number}'

    class Meta:
        verbose_name = _('Response')
        verbose_name_plural = _('Responses')


# @receiver(post_save, sender=Response)
# def change_ticket_status(sender, instance, created, **kwargs):
#     if created:
#         if instance.user.is_staff:
#             instance.ticket.status = 'support answer'
#             phone_number = instance.ticket.user.phone_number
#             ticketCode = instance.ticket.id
#             send_support_answer_ticket_sms_task.delay(phone_number, ticketCode)
#             instance.ticket.save()
#         else:
#             instance.ticket.status = 'user answer'
#             phone_number = instance.ticket.user.phone_number
#             ticketCode = instance.ticket.id
#             send_user_answer_ticket_sms_task.delay(phone_number, ticketCode)
#             instance.ticket.save()
