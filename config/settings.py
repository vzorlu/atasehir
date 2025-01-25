import os
from pathlib import Path
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv
from .template import TEMPLATE_CONFIG, THEME_LAYOUT_DIR, THEME_VARIABLES

load_dotenv()  # Load environment variables from .env.

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY", default="")
DEBUG = True
ALLOWED_HOSTS = ["atasehir.algi.ai", "localhost", "127.0.0.1", "148.251.52.194"]
# Django Environment
ENVIRONMENT = os.environ.get("DJANGO_ENVIRONMENT", default="local")

STATICFILES_DIRS = [
    BASE_DIR / "src" / "assets",
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.dashboards",
    "apps.layouts",
    "apps.front_pages",
    "apps.mail",
    "apps.chat",
    "apps.my_calendar",
    "apps.kanban",
    "apps.ecommerce",
    "apps.academy",
    "apps.logistics",
    "apps.invoice",
    "apps.users",
    "apps.access",
    "apps.pages",
    "apps.authentication",
    "apps.wizard_examples",
    "apps.modal_examples",
    "apps.cards",
    "apps.ui",
    "apps.extended_ui",
    "apps.icons",
    "apps.forms",
    "apps.form_layouts",
    "apps.form_wizard",
    "apps.form_validation",
    "apps.tables",
    "apps.charts",
    "apps.maps",
    "apps.transactions",
    "auth.apps.AuthConfig",
    "apps.containers",
    "apps.jobs",
    "apps.logs",
    "apps.notification",
    "django_extensions",
    "rest_framework",
    "devices",
    "customer",
    "services",
    "channels",
    "channels.layers",
    "stream",  # Add this line
    "council",
    "import_export",  # Add this line
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "web_project.language_middleware.DefaultLanguageMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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
                "config.context_processors.language_code",
                "config.context_processors.my_setting",
                "config.context_processors.get_cookie",
                "config.context_processors.environment",
            ],
            "libraries": {
                "theme": "web_project.template_tags.theme",
            },
            "builtins": [
                "django.templatetags.static",
                "web_project.template_tags.theme",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Update ASGI application path
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
"""

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

LANGUAGES = [
    ("en", _("English")),
    ("fr", _("French")),
    ("ar", _("Arabic")),
    ("de", _("German")),
]

LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [BASE_DIR / "locale"]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
BASE_URL = os.environ.get("BASE_URL", default="http://192.168.1.9:8000")
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# OneSignal Bildirim Ayarlar��
ONESIGNAL_APP_ID = "0a1a5cc3-275b-4d55-9137-e6304c066af0"
ONESIGNAL_API_KEY = "MjgwNTU2YTQtZGE0MC00ZTc4LTg3MzktYTRlZmM0MzMzM2M4"


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
print(GOOGLE_MAPS_API_KEY)
LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "/login/"

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 3600

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5050",
    "http://hub.algi.ai",
    "https://hub.algi.ai",
    "http://20.79.168.164/",
    "http://20.79.168.164:8000",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
    "https://atasehir.algi.ai",
    "http://148.251.52.194/http://192.168.1.9:8000",
]


THEME_LAYOUT_DIR = THEME_LAYOUT_DIR
TEMPLATE_CONFIG = TEMPLATE_CONFIG
THEME_VARIABLES = THEME_VARIABLES

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
}

CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

SECURE_SSL_REDIRECT = False
DATA_UPLOAD_MAX_NUMBER_FIELDS = 500000

# Import Export Settings
IMPORT_EXPORT_USE_TRANSACTIONS = True
IMPORT_EXPORT_SKIP_ADMIN_LOG = False
IMPORT_EXPORT_FORMATS = [
    "xlsx",
    "xls",
    "csv",
    "json",
]
