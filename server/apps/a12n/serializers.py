from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone

from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserSession



User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password',},
        min_length=8,
        )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password',},
        label='Confirm password',
    )
    email = serializers.EmailField(required=True,)
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password',
            'password_confirm',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('Passwords dont match')
        
        user_exists = User.objects.filter(
            Q(username=attrs['username']) | Q(email=attrs['email'])
        ).values('username', 'email')

        if user_exists.exists():
            raise serializers.ValidationError(
                'User with this username or email already exists'
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        )
    
    def validate(self, attrs):
        user = User.objects.filter(username=attrs['username']).first()
        if user is None or not user.check_password(attrs['password']):
            raise serializers.ValidationError('Invalid username or password')
        
        user_session = UserSession.objects.filter(user=user).all()
        if user_session.count() > 5:
            user_session.delete()

        return attrs
    
    def create(self, validated_data):
        user = validated_data['user']

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
        

class GenerateNewTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255,)
    fingerprint = serializers.CharField(max_length=255,)

    def validate(self, attrs):
        refresh_token = attrs.get('refresh_token')
        fingerprint = attrs.get('fingerprint')

        try:
            session = UserSession.objects.get(
                refresh_token=refresh_token,
                is_active=True,
            )
            attrs['session'] = session
        except UserSession.DoesNotExist:
            raise serializers.ValidationError('Invalid refresh token.')
        
        if timezone.now() > session.expires_in:
            raise serializers.ValidationError('Refresh token expired.')
        
        if session.fingerprint != fingerprint:
            raise serializers.ValidationError('Invalid fingerprint.')
        
        attrs['rotate_refresh'] = (
            session.expires_in - timezone.now()
            ).total_seconds() < 5*86400

        return attrs
    
    def save(self, **kwargs):
        refresh_token = RefreshToken(self.validated_data.get('refresh_token'))
        session = self.validated_data.get('session')
        
        if self.validated_data.get('rotate_refresh'):
            refresh_token = RefreshToken.for_user(session.user)
            refresh_token_lifetime = api_settings.REFRESH_TOKEN_LIFETIME
            session.refresh_token = refresh_token
            session.expires_in = timezone.now() + refresh_token_lifetime
            session.save()

        access_token = str(refresh_token.access_token)

        return {
            'refresh_token': str(refresh_token) if \
                self.validated_data.get('rotate_refresh') else None,
            'access_token': str(access_token),
        }