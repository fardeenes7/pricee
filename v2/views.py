from http.client import HTTPResponse
import json
import time
from django.shortcuts import render, redirect
from . import tasks
from django.http import HttpResponse as HTTPResponse
from .models import Product, Startech, Techland, Ryans, Category, SubCategory, Feature
from .serializers import *
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
    products = products.exclude(techland__isnull=True).exclude(startech__isnull=True).exclude(ryans__isnull=True)[(page-1)*16:page*16]
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ViewProductDetail(request, product_slug=-1):
    ifExists = Product.objects.filter(slug=product_slug).exists()
    if ifExists:
        product = Product.objects.get(slug=product_slug)
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
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    nav = {"categories": serializer.data, "shops": [
        {
            "name": "Techland",
            "href": "techland"
        },
        {
            "name": "Ryans",
            "href": "ryans"
        },
        {
            "name": "Startech",
            "href": "startech"
        }
    ]}
    return Response(nav)