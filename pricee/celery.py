from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from dotenv import load_dotenv
load_dotenv()



DEBUG = os.environ.get('DEBUG')
if DEBUG == 'True':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricee.settings.local')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricee.settings.production')


app = Celery('pricee')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()