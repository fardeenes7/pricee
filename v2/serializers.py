from rest_framework import serializers
from .models import *



class StartechSerializer(serializers.ModelSerializer):
    class Meta:
        model = Startech
        fields = ['link', 'price', 'regular_price', 'status', 'last_updated']


class RyansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ryans
        fields = ['link', 'price', 'regular_price', 'status', 'last_updated']

class TechlandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Techland
        fields = ['link', 'price', 'regular_price', 'status', 'last_updated']


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
    subcategories = SubCategoryListSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['name', 'slug', 'subcategories']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation




class ProductListSerializer(serializers.ModelSerializer):
    sub_category = SubcategorySerializer()
    
    class Meta:
        model = Product
        fields = ['name', 'slug', 'sub_category', 'best_price', 'brand', 'model', 'image']
        depth = 2


class ProductSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)
    sub_category = SubcategorySerializer()
    startech = StartechSerializer()
    ryans = RyansSerializer()
    techland = TechlandSerializer()
    
    class Meta:
        model = Product
        fields = ['name', 'sub_category', 'best_price', 'brand', 'model', 'image', 'startech', 'ryans', 'techland', 'features']
        depth = 2

