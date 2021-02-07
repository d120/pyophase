from .settings import *
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': os.environ['PORT'],
        'NAME': 'pyophase',
        'USER': 'root',
        'PASSWORD': 'pyophase',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
