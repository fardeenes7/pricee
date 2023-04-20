from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken
from rest_framework.parsers import MultiPartParser, FormParser


from .serializers import SocialAuthSerializer, EmailRegisterSerializer, EmailLoginSerializer




# Create your views here.

class SocialAuth(GenericAPIView):
    serializer_class = SocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validate_auth_token(request.data['auth_token']))
        
        return Response(data, status=status.HTTP_200_OK)



# create a class to return user details using access token
class UserView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated, ]
    # parser_classes = [MultiPartParser]

    def post(self, request):
        print(request.data)
        # if type(request.data['profile_pic']) == str:
        #     profile_pic = request.data.get('profile_pic', None)
        # else:
        #     None
        # if profile_pic is None:
        request_data = request.data.copy()
        request_data.pop('profile_pic', None)
        serializer = UserSerializer(request.user, data=request_data, partial=True)
        # else:
        #     serializer = UserSerializer(request.user, data=request.data)
        
            

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class EmailRegister(GenericAPIView):
    serializer_class = EmailRegisterSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validate(request.data)

        return Response(data, status=status.HTTP_200_OK)
       

class EmailLogin(GenericAPIView):
    serializer_class = EmailLoginSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validate(request.data)
        try:
            if data['error']:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data, status=status.HTTP_200_OK)


class ResetPassword(GenericAPIView):
    serializer_class = EmailLoginSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validate(request.data)
        try:
            if data['error']:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data, status=status.HTTP_200_OK)