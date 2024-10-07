from .models import User, Team
from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    UserUpdateSerializer
    )

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class UserListView(generics.ListAPIView):
    """
    Представление для получения списка пользователей.

    Методы:
    - GET: Возвращает список пользователей,фильтруя по имени
        пользователя, если оно передано в параметрах запроса.
    """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username', None)
        if username:
            queryset = queryset.filter(username__startswith=username)
        return queryset
    

class UserDetailView(generics.RetrieveAPIView):
    """
    Представление для получения деталей пользователя.

    Использует разные сериализаторы в зависимости от метода запроса:
    - UserDetailSerializer для GET-запросов.
    - UserUpdateSerializer для PUT и PATCH запросов.

    Методы:
    - GET: Возвращает информацию о пользователе.
    - PUT: Обновляет информацию о пользователе.
    - PATCH: Частично обновляет информацию о пользователе.
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserDetailSerializer

    def get_object(self):
        if self.kwargs.get('pk') == str(self.request.user.pk):
            return self.request.user
        return super().get_object()