from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from common.zarinpal import zarinpal_payment_request, zarinpal_payment_verify
from common.vandar import vandar_payment_request, vandar_payment_verify
from common.callback_gateway import callback_gateway
from posts.sitemap import PostSitemap
from pages.sitemap import PagesSitemap
from django.contrib.sitemaps import views
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView
from setting.models import Setting

sitemaps = {
    'posts': PostSitemap,
    'pages': PagesSitemap,
}


urlpatterns = [
    path('igadmini/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url='/static/icons/favicon.ico')),
    path('', include('pages.urls', namespace='pages')),
    path('services/', include('service.urls', namespace='services')),
    path('blog/', include('posts.urls', namespace='posts')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('comments/', include('comments.urls', namespace='comments')),
    path('dashboard/', include('accounts.urls', namespace='accounts')),
    path('callback-gateway/', callback_gateway, name='callback_gateway'),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('api/v1/', include('api.urls')),
    path(
        "sitemap.xml",
        views.index,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.index",
    ),
    path(
        "sitemap-<section>.xml",
        views.sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("robots.txt/", TemplateView.as_view(template_name="robots.txt",
         content_type="text/plain")),
    # path('iranian-instagram-followers/', lambda request: redirect('/', permanent=True)),

]

handler404 = 'pages.views.handling_404'


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


setting = Setting.objects.get(id=1)
if setting.active_payment_gateway == 'zarinpal':
    urlpatterns += path('payment-request/', zarinpal_payment_request, name='payment_request'),
    urlpatterns += path('payment-verify/', zarinpal_payment_verify, name='payment_verify'),
elif setting.active_payment_gateway == 'vandar':
    urlpatterns += path('payment-request/', vandar_payment_request, name='payment_request'),
    urlpatterns += path('payment-verify/', vandar_payment_verify, name='payment_verify'),