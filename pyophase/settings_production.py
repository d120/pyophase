"""
This is the settings file used in production.
First, it imports all default settings, then overrides respective ones.
Secrets are stored in and imported from an additional file, not set under version control.
"""

from pyophase.settings import *
import pyophase.settings_secrets as secrets

SECRET_KEY = secrets.SECRET_KEY

DEBUG = False

ALLOWED_HOSTS = ['.fachschaft.informatik.tu-darmstadt.de', '.d120.de']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'pyophase',
        'USER': 'pyophase',
        'PASSWORD': secrets.DB_PASSWORD
    }
}

STATIC_URL = '/ophasehq/static/'
LOGIN_URL = '/ophasehq/accounts/login/'

ADMINS = (('FSS', 'fss@fachschaft.informatik.tu-darmstadt.de'),)

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
