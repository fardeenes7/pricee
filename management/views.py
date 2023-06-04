from django.shortcuts import render
from .models import BannerAd
from django.utils import timezone
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
import datetime

from v2.models import Product
from user.models import User


# Create your views here.

class BannerAdAPIView(generics.ListAPIView):
    serializer_class = BannerAdSerializer
    pagination_class = None
    queryset = BannerAd.objects.filter(active=True).filter(scheduledFrom__lte=timezone.now()).filter(scheduledTo__gte=timezone.now()).order_by('-id')
    def get_queryset(self):
        banner1 = BannerAd.objects.filter(size='1x1', active=True).filter(scheduledFrom__lte=timezone.now()).filter(scheduledTo__gte=timezone.now()).order_by('-id')[:1]
        banner2 = BannerAd.objects.filter(size='3x1', active=True).filter(scheduledFrom__lte=timezone.now()).filter(scheduledTo__gte=timezone.now()).order_by('-id')[:1]
        if not banner1:
            banner1 = BannerAd.objects.filter(size='1x1', active=True).order_by('-id')[:1]
        if not banner2:
            banner2 = BannerAd.objects.filter(size='3x1', active=True).order_by('-id')[:1]
        if not banner1:
            banner1 = BannerAd.objects.filter(size='1x1').order_by('-id')[:1]
        if not banner2:
            banner2 = BannerAd.objects.filter(size='3x1').order_by('-id')[:1]
        banner = banner1 | banner2
        return banner




class checkAdminPermissionView(APIView):
    # permission_classes = [IsAuthenticated, ]

    def get(self, request):
        if request.user.is_staff:
            data = {'is_staff': True}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'is_staff': False}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
            
class CustomPageSizePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = manageProductListSerializer
    pagination_class = CustomPageSizePagination
    queryset = Product.objects.all().order_by('-id')


class ProductDetailView(APIView):
    # permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        serializer = manageProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        return Response(status=status.HTTP_200_OK)



class UserViewSet(viewsets.ModelViewSet):
    serializer_class = manageUserListSerializer
    pagination_class = CustomPageSizePagination
    queryset = User.objects.all().order_by('-id')



from user.auth.register import register_email_user
from rest_framework.parsers import MultiPartParser, FormParser

class UserCreateView(APIView):
    # permission_classes = [IsAuthenticated, ]
    def post(self, request):
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            data = {'message': 'Email already exist'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        name = request.data['name']
        password = request.data['password']
        provider = "email"
        username = request.data['username'] if 'username' in request.data else email.split('@')[0]
        image_url = request.data['image_url'] if 'image_url' in request.data else None
        print(request.data)
        data = register_email_user(provider, email, name, password, image_url, username)
        return Response(data, status=status.HTTP_200_OK)


# class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = manageUserCreationSerializer
    # permission_classes = [IsAuthenticated, ]

    # def post(self, request):
    #     #check email or username already exist
    #     if User.objects.filter(email=request.data['email']).exists():
    #         data = {'email': 'Email already exist'}
    #     elif User.objects.filter(username=request.data['username']).exists():
    #         data = {'username': 'Username already exist'}
    #     else:
    #         serializer = manageUserListSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             data = serializer.data
    #             return Response(data, status=status.HTTP_201_CREATED)
    #         else:
    #             data = serializer.errors
    #             return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
    #     return Response(data, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    # permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = manageUserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_200_OK)


class ReportView(APIView):
    def get(self, request):
        shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

from analytics.models import ProductView, LinkClick
class ReportGenerateView(APIView):
    def get(self, request):
        data = {}
        print(request.query_params)
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        shop = Shop.objects.get(pk=request.query_params.get('shopId'))
        queryset = Product.objects.filter(viewcount__date__month=month,viewcount__date__year=year).annotate(view_count=Count('viewcount__id')).order_by('-view_count')[:10]
        queryset = reportProductSerializer(queryset, many=True)
        data['mostVisitedProducts'] = queryset.data

        queryset = Link.objects.filter(linkclickcount__date__month=month,linkclickcount__date__year=year, shop=shop).annotate(click_count=Count('linkclickcount__id')).order_by('-click_count')[:10]
        queryset = reportLinkSerializer(queryset, many=True)
        data['mostClickedLinks'] = queryset.data

        print(data)

        return Response(data, status=status.HTTP_200_OK)

class DashboardView(APIView):
    def get(self, request):
        data = {'stats':{}, 'charts':[]}
        data['stats']['totalProducts'] = Product.objects.all().count()
        data['stats']['totalUsers'] = User.objects.all().count()
        data['stats']['totalProductViews'] = ProductView.objects.all().count()

        productViews = []
        for i in range(7):
            date = datetime.date.today()-datetime.timedelta(days=i)
            count = ProductView.objects.filter(date=date).count()
            productViews.append({'date': date.strftime("%d %b"), 'count': count})

        data['charts'].append({'title': 'Product Views','labels': [x['date'] for x in productViews], 'datasets':[{'title':"Product Views",'data': [x['count'] for x in productViews], 'backgroundColor': '#E86840'}]})

        #linkclickcount of last 7 days
        data['charts'].append({'title': 'External Link Clicks','labels': [x['date'] for x in productViews], 'datasets':[]})
        shops = Shop.objects.all()
        for shop in shops:
            linkClicks = []
            for i in range(7):
                date = datetime.date.today()-datetime.timedelta(days=i)
                count = LinkClick.objects.filter(date=date, link__shop=shop).count()
                linkClicks.append({'date': date.strftime("%d %b"), 'count': count})
            backgroundColor = '#72BF44' if shop.name == 'Ryans' else '#141D39' if shop.name == 'Techland' else '#EF4A23'
            data['charts'][1]['datasets'].append({'title':shop.name, 'data': [x['count'] for x in linkClicks], 'backgroundColor':backgroundColor})

        return Response(data, status=status.HTTP_200_OK)