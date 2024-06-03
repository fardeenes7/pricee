from .base import *
from dotenv import load_dotenv
load_dotenv()


DEBUG = True

ALLOWED_HOSTS = ['*']

# DATABASES = {
#     'default': {
#         #postgresql
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'pricee',
#         'USER': 'fardeen',
#         'PASSWORD': 'fardeen',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


import dj_database_url

DB_URL = os.environ.get('DATABASE_URL')

DATABASES = {
    'default': dj_database_url.config(
        # Feel free to alter this value to suit your needs.
        default=DB_URL,
        conn_max_age=600
    )
}