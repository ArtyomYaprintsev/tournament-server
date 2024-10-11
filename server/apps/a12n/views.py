from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegisterSerializer, UserLoginSerializer
from .models import UserSession
from apps.account.models import User

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import BadHeaderError, send_mail

from datetime import timezone


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            confirm_url = f'/confirm/{uid}/{token}'
            
            try:
                send_mail(
                    'Register confirm',
                    f'Hi, {user.username}, please confirm your registration,
                    follow this link: {confirm_url}',
                    'example@example.com',
                    [user.email],
                )
            except BadHeaderError:
                return Response(
                    {'detail': 'Error sending confirmation. Try again.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
            )

class LoginAPIView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            response = Response(
                {'access_token': data['access_token']},
                status=status.HTTP_200_OK
            )
            try:
                session = UserSession.objects.get(
                    refresh_token=data['refresh_token']
                )
                expires_at = session.expires_at
                max_age = (expires_at - timezone.now()).total_seconds()
            except UserSession.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST,)

            response.set_cookie(
                'refresh_token',
                data['refresh_token'],
                httponly=True,
                path= '/api/auth/',
                max_age=max_age,
            )
            return response
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
            )
    

class LogoutAPIView(APIView):
    
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            session = UserSession.objects.get(refresh_token=refresh_token)
            session.delete()
        except UserSession.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie(
            'refresh_token',
            path='/api/auth/',
        )
        return response