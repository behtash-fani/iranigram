from django.db import models
from django.utils.translation import gettext_lazy as _
import os
from django.contrib.auth import get_user_model


User = get_user_model()


def category_icon_path(instance, filename):
    # This function generates the file path where category icons will be stored
    return os.path.join('category_icons', f'{filename}')

class NotificationCategory(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    icon = models.FileField(upload_to=category_icon_path, blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

class Notification(models.Model):
    category = models.ForeignKey(NotificationCategory, on_delete=models.CASCADE, related_name='notifications', verbose_name=_('Category'))
    title = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('Title'))
    detail = models.TextField(blank=True, null=True, verbose_name=_('Detail'))
    readers = models.ManyToManyField(User, blank=True, related_name='read_notifications')
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
