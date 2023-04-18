from pathlib import Path
from datetime import timedelta
import os
from environs import Env

BASE_DIR = Path(__file__).resolve().parent.parent

# for environment variables
env = Env()
env.read_env()


SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG")
DJANGO_SITE_URL = env.list("DJANGO_SITE_URL")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

# Application definition

INSTALLED_APPS = [
    # "admin_persian",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_beat",
    "jalali_date",
    # 'django.contrib.humanize',
    "admin_reorder",
    # local apps
    "pages.apps.PagesConfig",
    "service.apps.ServiceConfig",
    "orders.apps.OrdersConfig",
    "accounts.apps.AccountsConfig",
    "transactions.apps.TransactionsConfig",
    "support.apps.SupportConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "admin_reorder.middleware.ModelAdminReorder",
    "django.middleware.security.SecurityMiddleware",
    # "pages.middleware.AdminLocaleMiddleware",
]

ADMIN_REORDER = (
    "sites",
    {"app": "accounts"},
    {"app": "orders"},
    {"app": "support"},
    {"app": "transactions"},
    {"app": "service"},
    {"app": "django_celery_beat"},
)

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.site_url.site_url",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get("POSTGRES_DATABASE"),
#         'USER': os.environ.get("POSTGRES_USER"),
#         'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
#         # 'HOST': os.environ.get('POSTGRES_HOST'),
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': 'db',
        'PORT': '5432',
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "fa-ir"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_L18N = True
USE_TZ = True
LOCALE_PATHS = (BASE_DIR / "templates/locale/",)

# Static files (CSS, JavaScript, Images)
# STATIC_URL = '/static/'
# if DEBUG:
#     STATICFILES_DIRS = [BASE_DIR / "static/"]
# else:
#     STATIC_ROOT = '/vol/static'


# # Base url to serve media files
# MEDIA_URL = '/static/ticket_files/'

# # Path where media is stored
# MEDIA_ROOT = '/vol/ticket_files'

STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / "static/"]
# STATIC_ROOT = BASE_DIR.parent / 'static'
STATIC_ROOT = os.path.join(BASE_DIR.parent, 'static')


MEDIA_URL = '/ticket_files/' 
MEDIA_ROOT = BASE_DIR.parent / 'ticket_files'

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"


# default settings (optional)
JALALI_DATE_DEFAULTS = {
    "Strftime": {
        "date": "%y/%m/%d",
        "datetime": "%H:%M:%S _ %y/%m/%d",
    },
    "Static": {
        "js": [
            # loading datepicker
            "admin/js/django_jalali.min.js",
        ],
        "css": {
            "all": [
                "admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css",
            ]
        },
    },
}

USE_L10N = True
# USE_THOUSAND_SEPARATOR = True
# THOUSAND_SEPARATOR = ','
# NUMBER_GROUPING = 3

# Zarinpal configuration
SANDBOX = env("ZARINPAL_SANDBOX")
MERCHANT = env("ZARINPAL_MERCHANT_ID")

if SANDBOX:
    sandbox = "sandbox"
else:
    sandbox = "www"

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = (
    f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
)
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


# Celery Configs
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_EXPIRES = timedelta(hours=2)
CELERY_TIMEZONE = TIME_ZONE

# Cache settings
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": "redis://redis:6379",
#     }
# }
