import os
from celery import Celery
from config.settings import base



if base.DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')


celery_app = Celery("config.settings")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
