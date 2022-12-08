from django.contrib import admin
from django.urls import path, re_path
from .views import *
#from django.conf.urls import url


#swagger api
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Pricee API",
      default_version='v1',
      description="API for Pricee",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="fardeen.es7@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('refreshAllRecords/', refreshAllRecords, name='refreshAllRecords'),
    path('all/', viewAllRecords, name='viewAllRecords'),
    path('products/all/', viewAllRecordsPagination, name='viewAllRecordsPagination'),
    path('products/all/<int:page>/', viewAllRecordsPagination, name='viewAllRecordsPagination'),
    path('categories/', CategoryList, name='CategoryList'),
      path('subcategories/', SubCategoryList, name='SubCategoryList'),
    

]
