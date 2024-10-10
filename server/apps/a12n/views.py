from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegisterSerializer, UserLoginSerializer
from .models import UserSession

from datetime import timezone


# class RegistrationAPIView(APIView):

#     def post(self, request):
#         serializer = UserRegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             refresh = RefreshToken.for_user(user)
#             refresh.payload.update({
#                 'user_id': user.id,
#                 'username': user.username
#             })
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }, status=status.HTTP_201_CREATED)
        

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