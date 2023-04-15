from .base import *
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent


ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ['*']
DJANGO_SITE_URL = "http://127.0.0.1:8000"



STATICFILES_DIRS = [
    BASE_DIR / "static/"
]