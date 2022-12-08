from http.client import HTTPResponse
import json
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
    tasks.refreshAllRecords.delay()
    return redirect('/admin')


@api_view(['GET'])
def viewAllRecords(request):
    products = Product.objects.all()[:50]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


#pagination
@api_view(['GET'])
def viewAllRecordsPagination(request, page=1):
    products = Product.objects.all()
    products = products.exclude(techland__isnull=True).exclude(startech__isnull=True).exclude(ryans__isnull=True)[(page-1)*16:page*16]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ViewProductDetail(request, product_id=-1):
    ifExists = Product.objects.filter(id=product_id).exists()
    if ifExists:
        product = Product.objects.get(id=product_id)
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