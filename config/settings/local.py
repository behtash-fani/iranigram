from .base import *
import os


ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ['*']




STATICFILES_DIRS = [
    BASE_DIR / "static/",
]