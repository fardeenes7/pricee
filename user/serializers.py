from rest_framework import serializers
from .auth.firebase import decode_token
from .auth.register import register_social_user, register_email_user
from .models import User
from django.contrib.auth import authenticate


class SocialAuthSerializer(serializers.Serializer):
    
        auth_token = serializers.CharField()
    
        def validate_auth_token(self, auth_token):
            user_data = decode_token(auth_token)
            print(user_data['firebase']['sign_in_provider'])
            try:
                user_data['uid']
            except:
                raise serializers.ValidationError('This token is either invalid or expired')

            if user_data['iss'] != 'https://securetoken.google.com/pricee-b2112':
                raise serializers.ValidationError('This token is either invalid or expired')
            email = user_data['email']
            name = user_data['name']
            if user_data['firebase']['sign_in_provider'] == 'google.com':
                provider = 'google'
            elif user_data['firebase']['sign_in_provider'] == 'facebook.com':
                provider = 'facebook'
            else:
                provider = 'email'
                
            uid = user_data['uid']
            image_url = user_data['picture'] if 'picture' in user_data else None
            return register_social_user(provider, uid, email, name, image_url)



class EmailRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    name = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', '')
        name = attrs.get('name', '')
        password = attrs.get('password', '')
        provider = 'email'
        return register_email_user(provider, email, name, password)

class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=255, min_length=3, read_only=True)

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = authenticate(email=email, password=password)
        if not user:
            return {
                'error': 'Invalid credentials, try again'
            }
        elif not user.is_active:
            return {
                'error': 'Account disabled, contact admin'
            }
        else:
            return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'profile_pic', 'name', 'bio', 'account_type', 'is_superuser', 'is_staff', 'is_active', 'date_joined')
        read_only_fields = ('id', 'date_joined')
