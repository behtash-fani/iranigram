from .base import *



ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')
CSRF_TRUSTED_ORIGINS = ['http://104.234.196.203']
