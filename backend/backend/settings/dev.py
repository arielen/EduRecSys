import os
from .base import *
from decouple import config, Csv

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())

# EMAIL CONFIG
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# SSL CONFIG
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SESSION_COOKIE_SECURE = config(
    'SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)

# DB CONFIG
DATABASES['default'] = {
    'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
    'NAME': config('DB_NAME', default=os.path.join(BASE_DIR, "db.sqlite3")),
    'USER': config('DB_USER', default=None),
    'PASSWORD': config('DB_PASSWORD', default=None),
    'HOST': config('DB_HOST', default=None),
    'PORT': config('DB_PORT', default=None),
}

try:
    from .local import *
except ImportError:
    pass
