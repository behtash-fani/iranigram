from .base import *


BASE_DIR = Path(__file__).resolve().parent.parent.parent



ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '104.234.196.203']
CSRF_TRUSTED_ORIGINS = 'http://104.234.196.203'
# DJANGO_SITE_URL = "http://104.234.196.203"

STATIC_ROOT = BASE_DIR / "static"