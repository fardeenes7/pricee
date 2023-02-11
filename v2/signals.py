from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
#from .tokens import account_activation_signup_token
from django.conf import Settings

from v1.tasks import refreshAllRecords

