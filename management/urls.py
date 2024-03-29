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
   path('dashboard/', DashboardView.as_view(), name='dashboard'),
   path('permission/',checkAdminPermissionView.as_view(), name='check_permission'),
   path('products', ProductViewSet.as_view({'get':'list'}), name='products'),
   path('products/<int:pk>', ProductDetailView.as_view(), name='product_detail'),

   path('users', UserViewSet.as_view({'get':'list'}), name='users'),  
   path('users/new', UserCreateView.as_view(), name='user_new'),  
   path('users/<int:pk>', UserDetailView.as_view(), name='user_detail'),

   path('report/', ReportView.as_view(), name='report_api'),
   path('report/generate/', ReportGenerateView.as_view(), name='report_api'),
   

]
