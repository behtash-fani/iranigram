from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class PagesSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0
    protocol = 'https'

    def items(self):
        return ['pages:home', 'pages:follower', 'pages:like', 'pages:view']

    def location(self, item):
        return reverse(item)
