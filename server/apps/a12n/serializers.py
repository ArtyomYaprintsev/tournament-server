from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings

from django.contrib.auth import authenticate
from django.utils import timezone
from django.conf import settings

from datetime import timezone

from apps.acсount.models import User
from .models import UserSession


# class UserRegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         style={'input_type': 'password',},
#         min_length=8,
#         )
#     password_confirm = serializers.CharField(
#         write_only=True,
#         required=True,
#         style={'input_type': 'password',},
#         lable='Confirm password',
#     )

#     class Meta:
#         model = User
#         fields = [
#             'username',
#             'first_name',
#             'lastname',
#             'password',
#             'password_confirm',
#         ]

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password_confirm']:
#             raise serializers.ValidationError('Passwords dont match')
#         return attrs

#     def create(self, validated_data):
#         validated_data.pop('password_confirm')
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        )
    
    def validate(self, attrs):
        user = User.objects.get(username=attrs['username']).first()
        if user is None or not user.check_password(attrs['password']):
            raise serializers.ValidationError('Invalid data')
        
        user_session = UserSession.objects.filter(user=user)
        if user_session.count() > 5:
            old_session = user_session.order_by('created_at').first()
            if old_session:
                old_session.delete()

        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        refresh_token_lifetime = api_settings.REFRESH_TOKEN_LIFETIME

        session = UserSession.objects.create(
            user=user,
            refresh_token=refresh_token,
            expires_in=timezone.now() + refresh_token_lifetime,
        )

        return {
            'refresh_token': str(refresh_token),
            'access_token': str(access_token),
        }