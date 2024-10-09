from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer

# Create your views here.
class RegistrationAPIView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({
                'user_id': user.id,
                'username': user.username
            })
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        

class LoginAPIView(APIView):

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        if username is None:
            return Response(
                {'error': 'username is required',},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if password is None:
            return Response(
                { 'error': 'password is required',},
                status=status.HTTP_401_UNAUTHORIZED
            )