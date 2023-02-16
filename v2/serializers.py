from rest_framework import serializers
from .models import *



class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'href', 'logo']

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


class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategoryListSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['name', 'slug', 'sub_categories']
        



class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['href']

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'href', 'logo', 'slug']


class LinkSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()
    class Meta:
        model = Link
        fields = ['shop', 'href', 'price', 'status']

class ProductListSerializer(serializers.ModelSerializer):
    sub_category = SubcategorySerializer()
    image = ImageSerializer(many=False, read_only=True)
    class Meta:
        model = Product
        fields = ['name', 'slug', 'sub_category', 'best_price', 'brand', 'model', 'image']
        depth = 2


class ProductSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)
    sub_category = SubcategorySerializer()
    class Meta:
        model = Product
        fields = ['name', 'sub_category', 'best_price', 'brand', 'model', 'images', 'links', 'features']
        depth = 2

