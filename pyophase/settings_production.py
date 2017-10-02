"""
This is the settings file used in production.
First, it imports all default settings, then overrides respective ones.
Secrets are stored in and imported from an additional file, not set under version control.
"""

from pyophase import settings_secrets as secrets

from .settings import *


SECRET_KEY = secrets.SECRET_KEY

DEBUG = False

ALLOWED_HOSTS = ['.fachschaft.informatik.tu-darmstadt.de', '.d120.de']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'pyophase',
        'USER': 'pyophase',
        'PASSWORD': secrets.DB_PASSWORD,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

STATIC_URL = '/ophase/static/'
LOGIN_URL = '/ophase/accounts/login/'
MEDIA_URL = '/ophase/media/'

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

ADMINS = (('pyophase-dev', 'pyophase-dev@fachschaft.informatik.tu-darmstadt.de'),)

SERVER_EMAIL = "pyophase@fachschaft.informatik.tu-darmstadt.de"
DEFAULT_FROM_EMAIL = SERVER_EMAIL

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.d120.de'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'pyophase'
EMAIL_HOST_PASSWORD = secrets.MAIL_PASSWORD

TUID_FORCE_SERVICE_URL = 'https://www.fachschaft.informatik.tu-darmstadt.de/ophase/sso/login/'

FILE_UPLOAD_PERMISSIONS = 0o644
