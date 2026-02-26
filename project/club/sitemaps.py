from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Names

class MemberSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Names.objects.all()

    def lastmod(self, obj):
        return obj.date_updated or obj.date_joined

    def location(self, obj):
        return obj.get_absolute_url()

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['club:main', 'club:members']

    def location(self, item):
        return reverse(item)
