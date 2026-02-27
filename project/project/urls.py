"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from club.sitemaps import MemberSitemap, StaticViewSitemap
from django.conf import settings
from django.conf.urls.static import static

sitemaps = {
    'members': MemberSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', include('club.urls', namespace='club')),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Custom error handlers
handler404 = 'club.views.custom_404'
handler500 = 'club.views.custom_500'

# Serve media files in development
# In production, configure your web server (Nginx/Apache) to serve media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
