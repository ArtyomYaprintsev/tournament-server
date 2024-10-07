from .models import User, Team
from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    UserUpdateSerializer
    )

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username', None)
        if username:
            queryset = queryset.filter(username__startswith=username)
        return queryset
    

class UserDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserDetailSerializer

    def get_object(self):
        return self.request.user
    

class AnotherUserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

