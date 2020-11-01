"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import braintree
import environ
import sentry_sdk

# from pathlib import Path
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# TODO migrate to Pathlib again and cast to str when necessary
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# django-environ
env = environ.Env(
    # # set casting, default value
    # DEBUG=(bool, False)
)

# Deploy NOTE defined first to decide when to read the .env file
DEPLOY = env("DEPLOY", str, None)

# reading .env file () when testing and in LOCAL env else read from env vars
if not DEPLOY or DEPLOY == "LOCAL":
    environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY", str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", bool, False)

ALLOWED_HOSTS = env("ALLOWED_HOSTS", tuple, ("localhost", "127.0.0.1"))


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "rosetta",
    "parler",
    "localflavor",
    # Local apps
    "dshop.shop.apps.ShopConfig",
    "dshop.cart.apps.CartConfig",
    "dshop.orders.apps.OrdersConfig",
    "dshop.payment.apps.PaymentConfig",
    "dshop.coupons.apps.CouponsConfig",
]

MIDDLEWARE = [
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "dshop.cart.context_processors.cart",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        # "ENGINE": "django.db.backends.sqlite3",
        # "NAME": BASE_DIR / "db.sqlite3",
        # "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
        "TEST": {"NAME": "xshop_test_db"},
        "CONN_MAX_AGE": 60 if DEPLOY != "LOCAL" else 0,
        "ATOMIC_REQUESTS": True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGES = (
    ("en", _("English")),
    ("es", _("Spanish")),
)
LANGUAGE_CODE = "en"
# LOCALE_PATHS = (BASE_DIR / "locale/",)
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale/"),)

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")

MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# cart
CART_SESSION_ID = "cart"

# email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Braintree settings
BRAINTREE_MERCHANT_ID = "rpj66nsdsndpr276"  # Merchant ID
BRAINTREE_PUBLIC_KEY = "wv983ydb62ymnw8z"  # Public Key
BRAINTREE_PRIVATE_KEY = "0750e26aa3bee1866dbb407bc4a3dcc3"  # Private key

BRAINTREE_CONF = braintree.Configuration(
    braintree.Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY,
)

# parler
PARLER_LANGUAGES = {
    None: (
        {"code": "en"},
        {"code": "es"},
    ),
    "default": {
        "fallback": "en",
        "hide_untranslated": False,
    },
}

# redis
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 1

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# sentry
if DEPLOY and DEPLOY not in ("LOCAL", "TESTING"):
    sentry_sdk.init(
        dsn=env("SENTRY_DSN", str),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )
