from .base import *
import os


ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000']



STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static/",
]