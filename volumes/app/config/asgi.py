import os
from django.core.asgi import get_asgi_application
from config.settings import base


if base.DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')


application = get_asgi_application()
