from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from common.zarinpal import payment_verify, payment_request
from common.callback_gateway import callback_gateway
from common.utils import send_otpcode_again
from posts.sitemap import PostSitemap
from pages.sitemap import PagesSitemap
from django.contrib.sitemaps import views
from django.views.generic import RedirectView


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
    path('payment-request/', payment_request, name='payment_request'),
    path('payment-verify/', payment_verify, name='payment_verify'),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('send-verify-code/', send_otpcode_again, name='send_verify_code'),
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
    path("robots.txt",include('robots.urls')),
    
]

handler404 = 'pages.views.handling_404'


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
