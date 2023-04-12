from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
from dotenv import dotenv_values
import os

load_dotenv()
config = dotenv_values(".env")
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.getenv('DEBUGMODE', False) == 'True'
SITE_URL = os.environ.get("DJANGO_SITE_URL")

# Application definition

INSTALLED_APPS = [
    "admin_persian",
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
                'config.site_url.site_url'
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": 5432,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = "fa-ir"
# TIME_ZONE = 'UTC'
TIME_ZONE = "Asia/Tehran"

USE_I18N = True
USE_L18N = True

USE_TZ = True

LOCALE_PATHS = (BASE_DIR / "templates/locale/",)


# Base url to serve media files
MEDIA_URL = "/ticket_files/"

# Path where media is stored
MEDIA_ROOT = BASE_DIR / "ticket_files/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

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
SANDBOX = os.environ.get("ZARINPAL_SANDBOX")
MERCHANT = os.environ.get("ZARINPAL_MERCHANT_ID")

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


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379",
    }
}