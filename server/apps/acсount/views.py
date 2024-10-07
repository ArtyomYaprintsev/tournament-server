from .models import User, Team
from .serializers import UserSerializer, TeamSerializer

from django.shortcuts import get_list_or_404

from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        pass