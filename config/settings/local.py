from .base import *
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent


ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ['*']




STATICFILES_DIRS = [
    BASE_DIR / "static/"
]