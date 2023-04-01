from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from .serializers import GoogleSocialAuthSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken



# Create your views here.

class GoogleSocialAuth(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validate_auth_token(request.data['auth_token']))
        
        return Response(data, status=status.HTTP_200_OK)



# create a class to return user details using access token
class UserView(APIView):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class Logout(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            # Delete all refresh tokens for the user
            # token.blacklist()
            # Delete all access tokens for the user
            # outstanding_tokens = OutstandingToken.objects.filter(user=token.user)
            # outstanding_tokens.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)