from .base import *
from dotenv import load_dotenv
load_dotenv()


DEBUG = True

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