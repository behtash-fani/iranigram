from django.db import models
from django.utils.translation import gettext_lazy as _




class PagesSeo(models.Model):
    page = models.CharField(_('Which Page'),max_length=255, blank=True, null=True)
    description_tag = models.TextField(_('Meta Description Tag'),blank=True, null=True)
    keywords_tag = models.CharField(_('Meta Keywords Tag'),max_length=255, blank=True, null=True)
    title_tag = models.CharField(_('Title Tag'),max_length=255, blank=True, null=True)


    def __str__(self): 
        return f'{self.page}'


    class Meta:
        verbose_name = _('SEO Setting')
        verbose_name_plural = _('SEO Settings')