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

from v2.models import Product
from user.models import User






# Create your views here.

def BannerAds(request):
    now = timezone.now()

    # First, get any scheduled ads that should be displayed.
    scheduled_ads = BannerAd.objects.filter(active=True, scheduledFrom__lte=now, scheduledTo__gte=now).order_by('-scheduledFrom')
    if scheduled_ads:
        banner = scheduled_ads.first()

    # If there are no scheduled ads, get the latest active ad.
    latest_active_ads = BannerAd.objects.filter(active=True).order_by('-id')
    if latest_active_ads:
        # Check which ad sizes we still need to display.
        sizes_needed = {'3x2': 1, '1x1': 2, '1x2': 1}
        for ad in latest_active_ads:
            if sizes_needed.get(ad.size):
                sizes_needed[ad.size] -= 1
                if all(count == 0 for count in sizes_needed.values()):
                    # We have all the ad sizes we need.
                    banner = ad
    data = banner
    #serialize data

class BannerAdAPIView(generics.GenericAPIView):
    serializer_class = BannerAdSerializer

    def get(self, request, *args, **kwargs):
        now = timezone.now()

        # First, get any scheduled ads that should be displayed.
        scheduled_ads = BannerAd.objects.filter(active=True, scheduledFrom__lte=now, scheduledTo__gte=now).order_by('-scheduledFrom')
        if scheduled_ads:
            banner = scheduled_ads.first()
            serializer = self.get_serializer(banner)
            return Response(serializer.data)

        # If there are no scheduled ads, get the latest active ad.
        latest_active_ads = BannerAd.objects.filter(active=True).order_by('-id')
        data = []
        if latest_active_ads:
            # Check which ad sizes we still need to display.
            sizes_needed = {'2x1': 1, '1x1': 2, '1x2': 1}
            for ad in latest_active_ads:
                if sizes_needed.get(ad.size):
                    sizes_needed[ad.size] -= 1
                    data.append(ad)
                    if all(count == 0 for count in sizes_needed.values()):
                        # We have all the ad sizes we need.
                        serializer = self.get_serializer(ad)
                        return Response(serializer.data)

        # If we get here, we couldn't find any ads to display.
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)



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


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = manageUserListSerializer
    pagination_class = CustomPageSizePagination
    queryset = User.objects.all().order_by('-id')



from user.auth.register import register_email_user

class UserCreateView(APIView):
    # permission_classes = [IsAuthenticated, ]
    def post(self, request):
        data = register_email_user(request.data)
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
        return Response(status=status.HTTP_200_OK)


class UserDeleteView(APIView):
    # permission_classes = [IsAuthenticated, ]

    # def get(self, request, pk):
    #     user = User.objects.get(pk=pk)
    #     user.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
