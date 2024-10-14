from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserSession
from .serializers import UserRegisterSerializer, UserLoginSerializer

User = get_user_model()

class RegistrationAPIView(APIView):
    """
    Представление для регистрации пользователя.

    Методы:
        - POST: Регистрирует пользователя и отправляет письмо с
        подтверждением регистрации.
    """
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
                {'detail': 'Account successfully created.'},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
            )


class ActivateAccountAPIView(APIView):
    """
    Представление для активации учетной записи пользователя
    по ссылке из письма.

    Методы:
        - GET: Активирует учетную запись пользователя и
        возвращает токены доступа.
    """
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist
        ):
            user = None

        if user is not None and \
        default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'detail': 'Acount successfully activated.',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'detail': 'Invalid token.'},
                status=status.HTTP_400_BAD_REQUEST,
                )

class LoginAPIView(APIView):
    """
    Представление для аутентификации пользователя и выдачи JWT токена.

    Методы:
        - POST: Принимает данные пользователя и возвращает при успешной
        аутентификации `access_token` в теле ответа и куки с `refresh_token`.
    """
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                session = UserSession.objects.get(
                    refresh_token=data['refresh_token']
                )
                expires_at = session.expires_at
                max_age = (expires_at - timezone.now()).total_seconds()
            except UserSession.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST,)
            
            response = Response(
                {'access_token': data['access_token']},
                status=status.HTTP_200_OK
            )
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
    """
    Представление для выхода пользователя из системы.

    Методы:
        - POST: Получает `refresh_token` из куки, затем удаляет
        сеанс пользователя.
    """
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            session = UserSession.objects.get(refresh_token=refresh_token)
            session.delete()
        except UserSession.DoesNotExist:
            return Response(
                {'detail': 'Invalid refresh token.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie(
            'refresh_token',
            path='/api/auth/',
        )
        return response