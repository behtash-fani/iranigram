from datetime import timedelta
from environs import Env
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
# for environment variables
env = Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool('DEBUG')
SITE_URL = env("DJANGO_SITE_URL")
if DEBUG:
    ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
else:
    ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")
AUTH_USER_MODEL = "accounts.User"
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django_celery_beat",
    "jalali_date",
    'django_ckeditor_5',
    "admin_reorder",
    "import_export",
    "rest_framework",
    'rest_framework.authtoken',
    # local apps
    "comments.apps.CommentsConfig",
    "pages.apps.PagesConfig",
    "service.apps.ServiceConfig",
    "orders.apps.OrdersConfig",
    "accounts.apps.AccountsConfig",
    "transactions.apps.TransactionsConfig",
    "support.apps.SupportConfig",
    "posts.apps.PostsConfig",
    "seo.apps.SeoConfig",
    "api.apps.ApiConfig",
    "setting.apps.SettingConfig",
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
    {"app": "comments"},
    {"app": "transactions"},
    {"app": "posts"},
    {"app": "service"},
    {"app": "seo"},
    {"app": "setting"},
    {"app": "django_celery_beat"},
    {"app": "authtoken"},
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
    STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.path.join(BASE_DIR.parent, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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


LOGOUT_REDIRECT_URL = "pages:home"
LOGIN_URL = "accounts:user_login_otp"

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '60/minute'
    },
    'EXCEPTION_HANDLER': 'api.custom_exception_handler.auth_exception_handler',
}

CKEDITOR_5_CUSTOM_CSS = '/static/django_ckeditor_5/src/override-django.css'
CKEDITOR_5_CONFIGS = {
    "default": {
        "language": {"ui": "fa", "content": "fa"},
        "contentLanguageDirection": "rtl",
        "fontFamily": {
            "options": [
                'default',
                'VazirMatn'
            ]
        },
        "alignment": {
            "options": ['left', 'right', 'center', 'justify']
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
                {
                    "model": "heading4",
                    "view": "h4",
                    "title": "Heading 4",
                    "class": "ck-heading_heading4",
                },
                {
                    "model": "heading5",
                    "view": "h5",
                    "title": "Heading 5",
                    "class": "ck-heading_heading5",
                },
                {
                    "model": "heading6",
                    "view": "h6",
                    "title": "Heading 6",
                    "class": "ck-heading_heading6",
                },
            ]
        },
        "toolbar": [
            "undo",
            "redo",
            "heading",
            "alignment",
            "fontSize",
            "fontFamily",
            "bold",
            "italic",
            "link",
            "underline",
            "mediaEmbed",
            "|",
            "outdent",
            "indent",
            "|",
            "codeBlock",
            "strikethrough",
            "code",
            "subscript",
            "superscript",
            "highlight",
            "|",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "blockQuote",
            "insertImage",
            "|",
            "fontColor",
            "fontBackgroundColor",
            "removeFormat",
            "insertTable",
            "sourceEditing",
        ],
    },
}


LOGS_DIR = os.path.join(BASE_DIR, 'logs')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime:s} {filename} {lineno:d} {name} {funcName} {process:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime:s} {module} {filename} {lineno:d} {funcName} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'custom_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'blogthedata.log'),
            'mode': 'a',
            'encoding': 'utf-8',
            'formatter': 'simple',
            'backupCount': 3,
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
        },
        'custom_handler_detailed': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'blogthedata_detailed.log'),
            'mode': 'a',
            'formatter': 'verbose',
            'backupCount': 3,
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console_handler', 'custom_handler_detailed'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['custom_handler'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
