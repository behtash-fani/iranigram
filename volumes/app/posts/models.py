from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from accounts.models import User



STATUS = (
    ("draft", _("Draft")),
    ("publish",_("Publish"))
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name=_("Title"))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_("Slug"))
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts', verbose_name=_("Author"), default='1')
    content = models.TextField(verbose_name=_("Content"))
    status = models.IntegerField(choices=STATUS, default=0,verbose_name=_("Status"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')