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
    class Meta:
        model = SubCategory
        fields = ['name', 'category']


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

