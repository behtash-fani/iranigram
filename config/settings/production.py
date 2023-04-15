from .base import *



ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = ['http://104.234.196.203']


STATIC_ROOT = "static/"