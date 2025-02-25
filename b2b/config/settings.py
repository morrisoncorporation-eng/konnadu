"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from dotenv import dotenv_values

config = dotenv_values(".env")  # load environment vars

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get("SECRET_KEY", os.environ.get("SECRET_KEY"))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["dj-b2b.herokuapp.com", "localhost", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.flatpages",
    "widget_tweaks",
    "cloudinary_storage",
    "cloudinary",
    "solo",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "sorl.thumbnail",
    "newsletter",
    "tinymce",
    "phonenumber_field",
    "django_user_agents",
    "djstripe",
    "django_htmx",
    "tempus_dominus",
    "main.apps.MainConfig",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django_user_agents.middleware.UserAgentMiddleware",
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
                "main.cart.context_processors.cart",
                "main.pages.context_processors.get_inner_categories",
                "main.dashboard.context_processors.new_arrival",
            ],
        },
    },
]

STRIPE_LIVE_SECRET_KEY = config.get(
    "STRIPE_LIVE_SECRET_KEY", os.environ.get("STRIPE_LIVE_SECRET_KEY")
)
STRIPE_TEST_SECRET_KEY = config.get(
    "STRIPE_TEST_SECRET_KEY", os.environ.get("STRIPE_TEST_SECRET_KEY")
)
STRIPE_PUBLISHABLE_KEY = config.get(
    "STRIPE_PUBLISHABLE_KEY", os.environ.get("STRIPE_PUBLISHABLE_KEY")
)
STRIPE_LIVE_MODE = False  # Change to True in production
DJSTRIPE_WEBHOOK_SECRET = "whsec_xxx"  # Get it from the section in the Stripe dashboard where you added the webhook endpoint
DJSTRIPE_USE_NATIVE_JSONFIELD = (
    True  # We recommend setting to True for new installations
)
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"  # Set to `"id"` for all new 2.4+ installations

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211",
    }
}

USER_AGENTS_CACHE = "default"

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

in_heroku = False
if "DATABASE_URL" in os.environ:
    in_heroku = True


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


LOGIN_REDIRECT_URL = "/customer/profile"

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

TEMPUS_DOMINUS_LOCALIZE = True

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = (str(BASE_DIR.joinpath("static")),)  # new
STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))  # new
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage' # new
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

if in_heroku:
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": config.get("CLOUD_NAME", os.environ.get("CLOUD_NAME")),
        "API_KEY": config.get("API_KEY", os.environ.get("API_KEY")),
        "API_SECRET": config.get("API_SECRET", os.environ.get("API_SECRET")),
    }
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_USER = config.get("EMAIL_USER", os.environ.get("EMAIL_USER"))
    EMAIL_HOST_PASSWORD = config.get("EMAIL_PASSWORD", os.environ.get("EMAIL_PASSWORD"))
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = "B2B"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config.get("DB_NAME"),
        "USER": config.get("DB_USER"),
        "PASSWORD": config.get("DB_PASSWORD"),
        "HOST": config.get("DB_HOST"),
        "PORT": config.get("DB_PORT"),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


import dj_database_url

prod_db = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(prod_db)
