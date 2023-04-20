from django.contrib import admin
from django.urls import path, re_path, include
from .views import *
#from django.conf.urls import url


#swagger api
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
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('manage/', include('management.urls')),

   path('refreshAllRecords/', refreshAllRecords, name='refreshAllRecords'),
   path('all/', viewAllRecords, name='viewAllRecords'),
   path('products', ProductViewSet.as_view({'get':'list'}), name='productviewset'),
   path('products/all/', viewAllRecordsPagination, name='viewAllRecordsPagination'),
   path('products/all/<int:page>/', viewAllRecordsPagination, name='viewAllRecordsPagination'),
   path('products/category/<str:category>/<int:page>', viewCategoryRecordsPagination, name='viewCategoryRecordsPagination'),
   path('products/subcategory/<str:subcategory>/<int:page>', viewSubCategoryRecordsPagination, name='viewSubCategoryRecordsPagination'),
   
   path('products/<str:product_slug>/', ViewProductDetail, name='ViewProductDetail'),
   path('products/record_view/<int:id>/', RecordProductView, name='RecordProductView'),


   path('categories/', CategoryList, name='CategoryList'),
   path('subcategories/', SubCategoryList, name='SubCategoryList'),
   path('navigation/', Navigation, name='Navigation'),

   path('landing', Landing, name='Landing'),


   #users api
   path('user/', include('user.urls')),
]