from django.urls import path, re_path
from .views import *

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Pricee API",
      default_version='v2',
      description="API for Pricee",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="fardeen.es7@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
   path('bannerads/', BannerAdAPIView.as_view(), name='bannerads'),
    

]
