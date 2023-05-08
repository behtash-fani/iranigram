from django.contrib.sitemaps import Sitemap
from .models import Post



class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9
    protocol = 'https'
    def items(self):
        return Post.objects.filter(status='publish')

    def lastmod(self, obj):
        return obj.updated_at