from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from accounts.models import User
# from ckeditor_uploader.fields import RichTextUploadingField




class Category(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    subtitle = models.CharField(max_length=20, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title



STATUS = (
    ("draft", _("Draft")),
    ("publish",_("Publish"))
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name=_("Title"), blank=True, null=True)
    slug = models.SlugField(max_length=900, unique=True, verbose_name=_("Slug"), blank=True, null=True, allow_unicode=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts', verbose_name=_("Author"), default='1')
    # content = RichTextUploadingField(verbose_name=_("Content"), blank=True, null=True)
    thumbnail = models.ImageField(upload_to='blog/', blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=0,verbose_name=_("Status"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'), blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'), blank=True, null=True)
    categories = models.ManyToManyField(Category,blank=True)
    status = models.CharField(max_length= 20, blank=True, null=True, choices=STATUS)
    

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')