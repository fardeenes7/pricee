from rest_framework import serializers
from .models import *
from v2.models import Image, Product


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
        fields = ['name', 'slug', 'sub_category', 'best_price', 'brand', 'model', 'image']
        depth = 2

    def get_image(self, product):
        images = product.images.all()
        if images.exists():
            return ImageSerializer(images.first()).data
        else:
            return None


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'sub_category', 'best_price', 'brand', 'model', 'images', 'num_views']
        depth = 2
