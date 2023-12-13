from django.db import models
from django.utils.translation import gettext_lazy as _


STATUS = (
    ("not approved", _("Not Approved")),
    ("approved", _("Approved")),
)


class Comment(models.Model):
    phone_number = models.CharField(max_length=13, verbose_name=_(
        'Phone Number'), blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name=_(
        'Name'), blank=True, null=True)
    content = models.TextField(verbose_name=_(
        'Content'), blank=True, null=True)
    page_id = models.CharField(verbose_name=_(
        'Page ID'), max_length=50, blank=True, null=True)
    page_url = models.CharField(verbose_name=_(
        'Page URL'), max_length=2000, blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS, verbose_name=_(
        'Status'), blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created At'), blank=True, null=True)
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Updated At'), blank=True, null=True)

    def __str__(self):
        return f'{self.phone_number}'

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class Response(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, verbose_name=_('comment'))
    phone_number = models.CharField(max_length=13, verbose_name=_(
        'Phone Number'), blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name=_(
        'Name'), blank=True, null=True)
    content = models.TextField(verbose_name=_(
        'Content'), blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS, verbose_name=_(
        'Status'), blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created At'), blank=True, null=True)
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Updated At'), blank=True, null=True)

    def __str__(self):
        return f'{self.comment.phone_number}'

    class Meta:
        verbose_name = _('Response')
        verbose_name_plural = _('Responses')

    def is_approved(self):
        return self.status == 'approved'
