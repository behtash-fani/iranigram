from .base import *


BASE_DIR = Path(__file__).resolve().parent.parent.parent


ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = ['http://104.234.196.203']


STATIC_ROOT = BASE_DIR / "static/"