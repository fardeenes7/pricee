from rest_framework import serializers
from .auth.firebase import decode_token
from .auth.register import register_social_user
from .models import User

class GoogleSocialAuthSerializer(serializers.Serializer):
    
        auth_token = serializers.CharField()
    
        def validate_auth_token(self, auth_token):
            user_data = decode_token(auth_token)
            try:
                user_data['uid']
            except:
                raise serializers.ValidationError('This token is either invalid or expired')

            if user_data['iss'] != 'https://securetoken.google.com/pricee-b2112':
                raise serializers.ValidationError('This token is either invalid or expired')
            print(user_data)
            email = user_data['email']
            name = user_data['name']
            provider = 'google'
            uid = user_data['uid']
            image_url = user_data['picture'] if 'picture' in user_data else None
            return register_social_user(provider, uid, email, name, image_url)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'profile_pic', 'name', 'bio', 'account_type', 'is_superuser', 'is_staff', 'is_active', 'date_joined')
        read_only_fields = ('id', 'date_joined')