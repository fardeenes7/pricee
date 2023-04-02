from django.urls import path
from .views import SocialAuth, UserView, Logout, EmailRegister, EmailLogin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
   path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
   path('', UserView.as_view(), name='user'),

   path('auth/social', SocialAuth.as_view(), name='social_auth'),
   path('auth/register', EmailRegister.as_view(), name='email_register'),
   path('auth/login', EmailLogin.as_view(), name='email_login'),
   path('auth/logout', Logout.as_view(), name='logout'),
]
