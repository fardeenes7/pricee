from django.urls import path
from .views import GoogleSocialAuth, UserView, Logout
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
   path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('', UserView.as_view(), name='user'),

   path('auth/google', GoogleSocialAuth.as_view(), name='google_social_auth'),
   # path('auth/facebook', FacebookSocialAuth.as_view(), name='facebook_social_auth'),
   path('auth/logout', Logout.as_view(), name='logout'),
]
