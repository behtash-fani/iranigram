from django.contrib.sitemaps import Sitemap
from django.urls import reverse



class PagesSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5
    def items(self):
        return ['pages:home','pages:follower','pages:like','pages:view']

    def location(self, item):
        return reverse(item)