from rest_framework import serializers
from .models import *
from v2.models import Image, Product, Shop, Link, Feature, SubCategory
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
        
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'href', 'logo', 'slug']


class LinkSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()
    clicks = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ['id', 'shop', 'href', 'price', 'status', 'last_updated', 'title', 'clicks']

    def to_representation(self, instance):
        formatted_last_updated = instance.last_updated.strftime("%d %b %Y %H:%M:%S")
        return {
            'id': instance.id,
            'shop': ShopSerializer(instance.shop).data,
            'href': instance.href,
            'price': instance.price,
            'status': instance.status,
            'last_updated': formatted_last_updated,
            'clicks': self.get_linkclickcount(instance),
        }
    def get_linkclickcount(self, instance):
        return instance.linkclickcount.count()

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['name', 'value']

class SubcategorySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    category_slug = serializers.SlugRelatedField(source='category', read_only=True, slug_field='slug')
    class Meta:
        model = SubCategory
        fields = ['name', 'slug', 'category', 'category_slug']


class manageProductDetailSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)
    sub_category = SubcategorySerializer()
    images = ImageSerializer(many=True, read_only=True)
    links = LinkSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'sub_category', 'best_price', 'brand', 'model', 'images', 'links', 'features']
        depth = 2
    




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