from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
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
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': [
        'https://rainbowchallenge.lt',
        "https://rainbowchallenge/auth/o/google-oauth2/",
        "http://127.0.0.1:8000/auth/o/google-oauth2/",
        "https://rainbowchallenge.lt/auth/users/me/",
        "https://rainbowchallenge.lt/api/user/oauth_token/"
    ]
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


PRIVATE_STORAGE_SERVER = 'django'
PRIVATE_STORAGE_INTERNAL_URL = None


CORS_REPLACE_HTTPS_REFERER = False
HOST_SCHEME = "http://"
SECURE_PROXY_SSL_HEADER = None
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = None
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_FRAME_DENY = False
#
# CORS_ALLOW_ALL_ORIGINS = True
