from .base import *
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent



ALLOWED_HOSTS = ['104.234.196.203', '127.0.0.1', 'localhost']
CSRF_TRUSTED_ORIGINS = ['http://104.234.196.203']
# DJANGO_SITE_URL = "http://104.234.196.203"

STATIC_ROOT = BASE_DIR / "static"

# ALLOWED_HOSTS = ["*"]
# CSRF_TRUSTED_ORIGINS = ['*']
# DJANGO_SITE_URL = "http://127.0.0.1:8000"



STATICFILES_DIRS = [
    BASE_DIR / "static/"
]