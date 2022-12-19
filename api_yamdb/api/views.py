from custom_user.models import User
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from reviews.models import Category, Genre, Title

from .mixins import ListCreateDestroyViewSet
from .permissions import IsAdmin, IsAdminOrReadOnly, UserPermission
from .serializers import (CategorySerializer, GenreSerializer, MeSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """Отображение действий с пользователями"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
        permission_classes=[UserPermission])

    def me(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = MeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriesViewSet(ListCreateDestroyViewSet):
    '''Работа с категориями для произведений'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    '''Работа с жанрами для произведений'''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Отображение действий с произведениями"""
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.all() # возможно где-то должна учитываться оценка
    pagination_class = PageNumberPagination
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer

