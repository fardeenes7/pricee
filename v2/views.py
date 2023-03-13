import json
import time
from django.shortcuts import render, redirect
from . import tasks
from django.http import HttpResponse
from .models import Product, Category, SubCategory, Feature
from .serializers import *
from rest_framework import viewsets
# Create your views here.

#rest framework
from rest_framework.decorators import api_view
from rest_framework.response import Response


def indexView(request):
    return render(request, 'index.html')

def refreshAllRecords(request):
    print("Refreshing All Records")
    tasks.adminActionRefreshAll(request)
    return redirect('/admin')


@api_view(['GET'])
def viewAllRecords(request):
    products = Product.objects.all()[:50]
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


#pagination
@api_view(['GET'])
def viewAllRecordsPagination(request, page=1):
    products = Product.objects.all()
    products = products[(page-1)*16:page*16]
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().exclude(best_price=0)
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.all().exclude(best_price=0)
        category = self.request.query_params.get('category', None)
        subcategory = self.request.query_params.get('sub_category', None)
        if category is not None:
            queryset = queryset.filter(sub_category__category__slug=category)
        if subcategory is not None:
            queryset = queryset.filter(sub_category__slug=subcategory)
        return queryset

@api_view(['GET'])
def viewCategoryRecordsPagination(request, page=1, category="all"):
    subcategories = SubCategory.objects.filter(category__slug=category) if category != "all" else SubCategory.objects.all()
    products = Product.objects.filter(sub_category__in=subcategories)
    products = products[(page-1)*16:page*16]
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def viewSubCategoryRecordsPagination(request, page=1, subcategory="all"):
    products = Product.objects.filter(sub_category__slug=subcategory) if subcategory != "all" else Product.objects.all()
    products = products[(page-1)*16:page*16]
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)




@api_view(['GET'])
def ViewProductDetail(request, product_slug=-1):
    ifExists = Product.objects.filter(slug=product_slug).exists()
    if ifExists:
        product = Product.objects.filter(slug=product_slug)[0]
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    else:
        return Response({"error": "Product not found"})


@api_view(['GET'])
def CategoryList(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def SubCategoryList(request):
    subcategories = SubCategory.objects.all()
    serializer = SubcategorySerializer(subcategories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def Navigation(request):
    exclude = ["Others", "Speaker", "Phone", "Home Appliance", "Home Appliances", "Digital Signage"]
    categories = Category.objects.all().exclude(name__in=exclude).order_by('name')
    serializer = CategorySerializer(categories, many=True)
    shops = Shop.objects.all()
    shopSerializer = ShopSerializer(shops, many=True)
    nav = {"categories": serializer.data, "shops": shopSerializer.data}
    return Response(nav)



from management.models import BannerAd
from management.serializers import BannerAdSerializer

@api_view(['GET'])
def Landing(request):
    bannerAds = []
    bannerAds.append(BannerAd.objects.filter(active=True, size='3x1').order_by('-id')[0])
    bannerAds.append(BannerAd.objects.filter(active=True, size='1x1').order_by('-id')[0])
    bannerAdSerializer = BannerAdSerializer(bannerAds, many=True)

    categories = Category.objects.all()[:8]
    categorySerializer = LandingCategorySerializer(categories, many=True)

    products = Product.objects.all().exclude(best_price=0)[:20]
    productSerializer = ProductListSerializer(products, many=True)

    return Response({"bannerAds": bannerAdSerializer.data, "categories": categorySerializer.data, "products": productSerializer.data})
