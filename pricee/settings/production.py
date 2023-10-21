from .base import *
import os
import dj_database_url

name = os.environ.get('DB_NAME')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')
DB_URL = os.environ.get('DATABASE_URL')

DEBUG = False

ALLOWED_HOSTS = ['*']

# DATABASES = {
#     'default': {
#         #postgresql
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': name,
#         'USER': user,
#         'PASSWORD': password,
#         'HOST': host,
#         'PORT': port,
#     }
# }

DATABASES = {
    'default': dj_database_url.config(
        # Feel free to alter this value to suit your needs.
        default=DB_URL,
        conn_max_age=600
    )
}