from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_support_answer_ticket_sms_task, send_user_answer_ticket_sms_task


STATUS = (
    ("submitted", _("submitted")),
    ("closed", _("closed")),
    ("pending", _("pending")),
    ("support answer", _("support answer")),
    ("user answer", _("user answer")),
)


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    subject = models.CharField(max_length=50, verbose_name=_('Subject'))
    message = models.TextField(verbose_name=_('Message'))
    status = models.CharField(max_length=30, choices=STATUS, verbose_name=_('Status'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    file = models.ImageField(upload_to='ticket/', blank=True, null=True, verbose_name=_('File'))

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')


class Response(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name=_('Ticket'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name=_('User'))
    message = models.TextField(verbose_name=_('Message'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    file = models.FileField(blank=True, null=True, verbose_name=_('File'))

    def __str__(self):
        return self.ticket.subject

    class Meta:
        verbose_name = _('Response')
        verbose_name_plural = _('Responses')


@receiver(post_save, sender=Response)
def change_ticket_status(sender, instance, created, **kwargs):
    if created:
        if instance.user.is_staff:
            instance.ticket.status = 'support answer'
            phone_number = instance.ticket.user.phone_number
            ticketCode = instance.ticket.id
            send_support_answer_ticket_sms_task.delay(phone_number, ticketCode)
            instance.ticket.save()
        else:
            instance.ticket.status = 'user answer'
            phone_number = instance.ticket.user.phone_number
            ticketCode = instance.ticket.id
            send_user_answer_ticket_sms_task.delay(phone_number, ticketCode)
            instance.ticket.save()
