"""
Django settings for rainbow project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os

from pathlib import Path

from dotenv import load_dotenv
from firebase_admin import initialize_app

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

INSTALLED_APPS = [
    # 'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    # third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'social_django',
    'drf_spectacular',
    'django_extensions',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'nested_inline',
    'widget_tweaks',
    'private_storage',
    'corsheaders',
    'django_advanced_password_validation',
    'import_export',
    'fcm_django',

    # project apps
    'user',
    'results',
    'challenge',
    'joined_challenge',
    'news',
    'message',
    'quiz',
    'texts',
    'dashboard',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
]

ROOT_URLCONF = 'rainbow_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rainbow_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_USER = os.environ.get('DB_USER')
DB_HOST = os.environ.get('DB_HOST')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rainbow',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '5432',
        # 'OPTIONS': {
        #     'read_default_file': '/path/to/my.cnf',
        # },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'django_advanced_password_validation.advanced_password_validation.ContainsDigitsValidator',
        'OPTIONS': {
            'min_digits': 1
        }
    },
    {
        'NAME': 'django_advanced_password_validation.advanced_password_validation.ContainsUppercaseValidator',
        'OPTIONS': {
            'min_uppercase': 1
        }
    },
    {
        'NAME': 'django_advanced_password_validation.advanced_password_validation.ContainsLowercaseValidator',
        'OPTIONS': {
            'min_lowercase': 1
        }
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'lt-lt'

TIME_ZONE = 'Europe/Vilnius'
# USE_DEPRECATED_PYTZ = True

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
SITE_ID = 1
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'), ]

# for local development
STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'static'),
)

AUTH_USER_MODEL = 'user.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password_reset/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'SERIALIZERS': {
        'user': 'user.serializers.UserSerializer',
        'user_create': 'user.serializers.CustomUserCreateSerializer',
        'user_create_password_retype': 'user.serializers.CustomUserCreateSerializer',
        'current_user': 'user.serializers.UserSerializer',
    },
    'LOGIN_FIELD': 'email',
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'USER_ID_FIELD': 'uid',
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': False,

    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': [
        'https://rainbowchallenge.lt',
        "https://rainbowchallenge/auth/o/google-oauth2/",
        "http://127.0.0.1:8000/auth/o/google-oauth2/",
        "https://rainbowchallenge.lt/auth/users/me/",
        "https://rainbowchallenge.lt/api/user/oauth_token/"
    ]
}

# SOCIAL AUTHENTICATION

# enabling because of social_django
SOCIAL_AUTH_JSONFIELD_ENABLED = True

AUTHENTICATION_BACKENDS = (
    # We are going to implement Google, choose the one you need from docs
    'social_core.backends.google.GoogleOAuth2',

    # Crucial when logging into admin with username & password
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

# this is to avoid an error about missing state
# SESSION_COOKIE_SAMESITE = None
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['state']
SESSION_COOKIE_SECURE = False
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True


SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
)

# OTP token login

OTP_TOTP_ISSUER = 'Rainbow challenge'

# EMAIL

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


# SSL/TLS

CORS_REPLACE_HTTPS_REFERER = True
HOST_SCHEME = "https://"
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 1000000
SECURE_FRAME_DENY = True


ADMIN_EMAILS = os.environ.get("ADMIN_EMAILS").split(",")

# FILES


# max file size - 20 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 20971520

PRIVATE_STORAGE_ROOT = os.path.join(BASE_DIR, 'media-private')
PRIVATE_STORAGE_AUTH_FUNCTION = 'private_storage.permissions.allow_staff'
PRIVATE_STORAGE_SERVER = 'nginx'
PRIVATE_STORAGE_INTERNAL_URL = '/private-x-accel-redirect/'


# LOGGING

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django-logfile'),
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'logfile']
    },
}

# FIREBASE

# Firebase settings, provided by Google

import firebase_admin
# from firebase_admin import credentials
#
# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)


# Optional ONLY IF you have initialized a firebase app already:
# Visit https://firebase.google.com/docs/admin/setup/#python
# for more options for the following:
# Store an environment variable called GOOGLE_APPLICATION_CREDENTIALS
# which is a path that point to a json file with your credentials.
# Additional arguments are available: credentials, options, name
FIREBASE_APP = firebase_admin.initialize_app()
# To learn more, visit the docs here:
# https://cloud.google.com/docs/authentication/getting-started>

FCM_DJANGO_SETTINGS = {
     # an instance of firebase_admin.App to be used as default for all fcm-django requests
     # default: None (the default Firebase app)
     "DEFAULT_FIREBASE_APP": None,
     # default: _('FCM Django')
     # "APP_VERBOSE_NAME": "[string for AppConfig's verbose_name]",
     # true if you want to have only one active device per registered user at a time
     # default: False
     "ONE_DEVICE_PER_USER": False,
     # devices to which notifications cannot be sent,
     # are deleted upon receiving error response from FCM
     # default: False
     "DELETE_INACTIVE_DEVICES": False,
     # Transform create of an existing Device (based on registration id) into
     # an update. See the section
     # "Update of device with duplicate registration ID" for more details.
     # default: False
     "UPDATE_ON_DUPLICATE_REG_ID": True,
}
