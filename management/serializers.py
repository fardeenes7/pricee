from rest_framework import serializers
from .models import *
from v2.models import Image, Product
from user.models import User


class BannerAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerAd
        fields = ['image', 'title', 'slug', 'size']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['href']



class manageProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','name', 'slug', 'sub_category', 'best_price', 'brand', 'model', 'image']
        depth = 2

    def get_image(self, product):
        images = product.images.all()
        if images.exists():
            return ImageSerializer(images.first()).data
        else:
            return None



class manageUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','profile_pic','account_type', 'email', 'name', 'is_active']
        depth = 1


class manageUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "name", "bio", "account_type", "auth_provider", "profile_pic", "is_superuser", "is_staff", "is_active", "date_joined", "groups", "user_permissions", "last_login"]
        depth = 1

class manageUserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "name", "bio", "account_type", "auth_provider", "profile_pic", "is_superuser", "is_staff", "is_active", "date_joined", "groups", "user_permissions", "last_login"]
        depth = 1