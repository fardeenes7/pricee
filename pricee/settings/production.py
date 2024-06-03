from .base import *
import os
import dj_database_url

DB_URL = os.environ.get('DATABASE_URL')

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': dj_database_url.config(
        # Feel free to alter this value to suit your needs.
        default=DB_URL,
        conn_max_age=600
    )
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build')
STATICFILES_STORAGE="whitenoise.storage.CompressedManifestStaticFilesStorage"