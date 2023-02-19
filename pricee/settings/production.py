from .base import *


DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        #postgresql
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pricee',
        'USER': 'fardeen',
        'PASSWORD': 'fardeen',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}