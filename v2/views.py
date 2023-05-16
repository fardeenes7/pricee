import json
import time
from django.shortcuts import render, redirect
from . import tasks
from django.http import HttpResponse
from .models import Product, Category, SubCategory, Feature, Link
from .serializers import *
from rest_framework import viewsets, status
from django.db.models import Count, Sum, Case, When, IntegerField
from rest_framework.generics import ListAPIView


#Analytics
from analytics.models import ProductView, CategoryView, LinkClick

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


# #pagination
# @api_view(['GET'])
# def viewAllRecordsPagination(request, page=1):
#     products = Product.objects.annotate(num_views=Count('viewcount')).order_by('-num_views')
#     products = products[(page-1)*16:page*16]
#     serializer = ProductListSerializer(products, many=True)
#     return Response(serializer.data)


@api_view(['GET'])
def viewAllRecordsPagination(request, page=1):
    if request.user.is_authenticated:
        top_categories = SubCategory.objects.annotate(num_views=Sum(
            Case(When(categoryviewcount__user=request.user, then=1),
                 default=0, output_field=IntegerField()))).order_by('-num_views')[:5]
        products = Product.objects.filter(sub_category__in=top_categories).annotate(num_views=Count('viewcount')).order_by('-num_views')
    else:
        products = Product.objects.annotate(num_views=Count('viewcount')).order_by('-num_views')
    products = products[(page-1)*16:page*16]
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


# class ProductViewSet(viewsets.ModelViewSet):
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class ProductViewSet(ListAPIView):
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name','best_price']
    search_fields = ['name', 'sub_category__category__name', 'sub_category__name']
    order_fields = ['name', 'best_price']

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        subcategory = self.request.query_params.get('sub_category', None)
        search = self.request.query_params.get('search', None)

        if self.request.user.is_authenticated and category is None  and subcategory is None and search is None:
            queryset = Product.objects.filter(viewcount__user=self.request.user).annotate(num_views=Count('viewcount')).order_by('-num_views').exclude(best_price=0)
            top_categories = SubCategory.objects.filter(
                categoryviewcount__user=self.request.user).annotate(num_views=Count('categoryviewcount')
            ).order_by('-num_views')[:5]
            queryset = queryset.filter(sub_category__in=top_categories)
        elif search is None:
            queryset = Product.objects.annotate(num_views=Count('viewcount')).order_by('-num_views').exclude(best_price=0)
        else:
            queryset = Product.objects.annotate(num_views=Count('viewcount')).order_by('-num_views')

        if category is not None:
            queryset = queryset.filter(sub_category__category__slug=category)
        if subcategory is not None:
            queryset = queryset.filter(sub_category__slug=subcategory)
        return queryset


# class ProductListAPIView(ListAPIView):
#     def get_queryset(self):
#     serializer_class = ProductListSerializer
#     category = self.request.query_params.get('category', None)
#     subcategory = self.request.query_params.get('sub_category', None)
#     search = self.request.query_params.get('query', None)
#     if self.request.user.is_authenticated and category is None  and subcategory is None:
#             queryset = Product.objects.filter(viewcount__user=self.request.user).annotate(num_views=Count('viewcount')).order_by('-num_views').exclude(best_price=0)
#             top_categories = SubCategory.objects.filter(
#                 categoryviewcount__user=self.request.user).annotate(num_views=Count('categoryviewcount')
#             ).order_by('-num_views')[:5]
#             queryset = queryset.filter(sub_category__in=top_categories)
#     else:
#         queryset = Product.objects.annotate(num_views=Count('viewcount')).order_by('-num_views').exclude(best_price=0)

#     if category is not None:
#         queryset = queryset.filter(sub_category__category__slug=category)
#     if subcategory is not None:
#         queryset = queryset.filter(sub_category__slug=subcategory)
    

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
        user = request.user if request.user.is_authenticated else None
        # ProductView.objects.create(product=product, user=user)
        # CategoryView.objects.create(category=product.sub_category, user=user)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    else:
        return Response({"error": "Product not found"})

@api_view(['POST'])
def RecordProductView(request, id):
    ifExists = Product.objects.filter(id=id).exists()
    if ifExists:
        product = Product.objects.filter(id=id)[0]
        user = request.user if request.user.is_authenticated else None
        ProductView.objects.create(product=product, user=user)
        CategoryView.objects.create(category=product.sub_category, user=user)
        return Response({"status":200}, status=status.HTTP_200_OK)
    else:
        return Response({"status": 400}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def RecordLinkClick(request, id):
    ifExists = Link.objects.filter(id=id).exists()
    if ifExists:
        link = Link.objects.filter(id=id)[0]
        user = request.user if request.user.is_authenticated else None
        LinkClick.objects.create(link=link, user=user)
        return Response({"status":200}, status=status.HTTP_200_OK)
    else:
        return Response({"status": 400}, status=status.HTTP_400_BAD_REQUEST)




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

    products = Product.objects.annotate(num_views=Count('viewcount')).order_by('-num_views').exclude(best_price=0)[:20]
    productSerializer = ProductListSerializer(products, many=True)

    return Response({"bannerAds": bannerAdSerializer.data, "categories": categorySerializer.data, "products": productSerializer.data})
