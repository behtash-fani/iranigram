from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from utils.zarinpal import payment_verify, payment_request
from utils.callback_gateway import callback_gateway

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls', namespace='pages')),
    path('services/', include('service.urls', namespace='services')),
    # path('blog/', include('posts.urls', namespace='posts')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('dashboard/', include('accounts.urls', namespace='accounts')),
    path('callback-gateway/', callback_gateway, name='callback_gateway'),
    path('payment-request/', payment_request, name='payment_request'),
    path('payment-verify/', payment_verify, name='payment_verify'),
    # path('ckeditor', include('ckeditor_uploader.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
