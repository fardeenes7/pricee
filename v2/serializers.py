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

    # def to_representation(self, instance):
    #     return super().to_representation(instance)

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'href', 'logo', 'slug']


class LinkSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()
    class Meta:
        model = Link
        fields = ['id', 'shop', 'href', 'price', 'status', 'last_updated', 'title']

    def to_representation(self, instance):
        formatted_last_updated = instance.last_updated.strftime("%d %b %Y %H:%M:%S")
        return {
            'id': instance.id,
            'shop': ShopSerializer(instance.shop).data,
            'href': instance.href,
            'price': instance.price,
            'status': instance.status,
            'last_updated': formatted_last_updated
        }

class ProductListSerializer(serializers.ModelSerializer):
    sub_category = SubcategorySerializer()
    image = serializers.SerializerMethodField()
    num_views = serializers.IntegerField()
    class Meta:
        model = Product
        fields = ['name', 'slug', 'sub_category', 'best_price', 'brand', 'model', 'image', 'num_views']
        depth = 2

    def get_image(self, product):
        images = product.images.all()
        if images.exists():
            return ImageSerializer(images.first()).data
        else:
            return None


class SuggestionsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['name', 'slug', 'best_price', 'brand', 'model', 'image']
        depth = 2

    def get_image(self, product):
        images = product.images.all()
        if images.exists():
            return ImageSerializer(images.first()).data
        else:
            return None


class ProductSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)
    sub_category = SubcategorySerializer()
    images = ImageSerializer(many=True, read_only=True)
    suggestions = serializers.SerializerMethodField()
    links = LinkSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'sub_category', 'best_price', 'brand', 'model', 'images', 'links', 'features', 'suggestions']
        depth = 2
    
    def get_suggestions(self, product):
        suggestions = Product.objects.filter(sub_category=product.sub_category).exclude(id=product.id).order_by('?')[:6]
        return SuggestionsSerializer(suggestions, many=True).data






# Landing Page Serializers

class LandingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']