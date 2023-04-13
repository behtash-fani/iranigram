from .base import *
import os


ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ['*']



STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static/",
]