from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from accounts.models import User
import readtime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

class Category(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


STATUS = (
    ("draft", _("Draft")),
    ("publish",_("Publish"))
)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts', verbose_name=_("Author"), default='1')
    title = models.CharField(max_length=200, unique=True, verbose_name=_("Title"), blank=True, null=True)
    slug = models.SlugField(max_length=900, unique=True, verbose_name=_("Slug"), blank=True, null=True, allow_unicode=True)
    short_content = models.CharField(max_length=170, verbose_name=_("Short Content"), blank=True, null=True)
    content = CKEditor5Field(verbose_name=_("Content"), blank=True, null=True)
    read_time = models.CharField(max_length=100, verbose_name=_("Read Time"), blank=True, null=True)
    thumbnail = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name=_("Thumbnail"))
    status = models.IntegerField(choices=STATUS, default=0,verbose_name=_("Status"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'), blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'), blank=True, null=True)
    category = models.ForeignKey(Category,verbose_name=_('Category'), blank=True, null=True, on_delete= models.DO_NOTHING)
    status = models.CharField(max_length= 20, blank=True, null=True, choices=STATUS)
    

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'slug':self.slug})

@receiver(post_save, sender=Post)
def check_read_time(sender, instance, created, **kwargs):
    read_time = readtime.of_text(str(instance.content))
    Post.objects.filter(id=instance.id).update(read_time=read_time.minutes)        


# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_("Blog Post"), related_name='comments')
#     author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE)
#     text = models.TextField(verbose_name=_("Text"))
#     created_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

#     def __str__(self):
#         return f'{self.author.username} - {self.text[:50]}'