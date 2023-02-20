from rest_framework import serializers
from .models import *


class BannerAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerAd
        fields = ['image', 'title', 'slug', 'size']