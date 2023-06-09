from pathlib import Path
from datetime import timedelta
import os
from environs import Env
import logging

BASE_DIR = Path(__file__).resolve().parent.parent

# for environment variables
env = Env()
env.read_env()


SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG")
SITE_URL = env("DJANGO_SITE_URL")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")
SUBMIT_AUTOMATIC_ORDERS=env.bool("SUBMIT_AUTOMATIC_ORDERS")

# Application definition

INSTALLED_APPS = [
    "admin_persian",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    "django_celery_beat",
    "jalali_date",
    'ckeditor',
    'ckeditor_uploader',
    "admin_reorder",
    # 'django_redis',
    # local apps
    "pages.apps.PagesConfig",
    "service.apps.ServiceConfig",
    "orders.apps.OrdersConfig",
    "accounts.apps.AccountsConfig",
    "transactions.apps.TransactionsConfig",
    "support.apps.SupportConfig",
    "posts.apps.PostsConfig",
    "seo.apps.SeoConfig",
    
]
SITE_ID = 1

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
]

ADMIN_REORDER = (
    {"app": "accounts"},
    {"app": "orders"},
    {"app": "support"},
    {"app": "transactions"},
    {"app": "service"},
    {"app": "seo"},
    {"app": "posts"},
    {"app": "django_celery_beat"},
    {"app": "admin_persian"},
    {"app": "sites"},
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

STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / "static/"]
STATIC_ROOT = os.path.join(BASE_DIR.parent, 'static')


MEDIA_URL = '/media/' 
MEDIA_ROOT = BASE_DIR / 'media'
CKEDITOR_UPLOAD_PATH = "blog/"
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
THOUSAND_SEPARATOR = ','
NUMBER_GROUPING = 3

# Zarinpal configuration
SANDBOX = env.bool("ZARINPAL_SANDBOX")
MERCHANT = env("ZARINPAL_MERCHANT_ID")

if SANDBOX:
    sandbox = "sandbox"
else:
    sandbox = "www"

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
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
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379',
    }
}


LOGOUT_REDIRECT_URL="pages:home"
LOGIN_URL = "accounts:user_login_otp"

if not DEBUG:
    FORMATTERS = (
        {
            "verbose": {
                "format": "{levelname} {asctime:s} {threadName} {thread:d} {module} {filename} {lineno:d} {name} {funcName} {process:d} {message}",
                "style": "{",
            },
            "simple": {
                "format": "{levelname} {asctime:s} {module} {filename} {lineno:d} {funcName} {message}",
                "style": "{",
            },
        },
    )


    HANDLERS = {
        "console_handler": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "my_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": f"{BASE_DIR}/logs/igthedata.log",
            "mode": "a",
            "encoding": "utf-8",
            "formatter": "simple",
            "backupCount": 5,
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
        },
        "my_handler_detailed": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": f"{BASE_DIR}/logs/igthedata_detailed.log",
            "mode": "a",
            "formatter": "verbose",
            "backupCount": 5,
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
        },
        'celery_task': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f"{BASE_DIR}/logs/celery_task.log",
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
            "mode": "a",
        }
    }

    LOGGERS = (
        {
            "django": {
                "handlers": ["console_handler", "my_handler_detailed"],
                "level": "INFO",
                "propagate": False,
            },
            "django.request": {
                "level": "INFO",
                "propagate": False,
            },
            "my_logger": {
                "handlers": ["my_handler"],
                "level": "INFO",
                "propagate": False,
            },
            'celery_task': {
                'handlers': ["celery_task"],
                'level': 'INFO',
                "propagate": False,
            },
        },
    )


    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": FORMATTERS[0],
        "handlers": HANDLERS,
        "loggers": LOGGERS[0],
    }
