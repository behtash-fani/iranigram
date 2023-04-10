import os
from config.settings import base


from django.core.wsgi import get_wsgi_application

if base.DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()
