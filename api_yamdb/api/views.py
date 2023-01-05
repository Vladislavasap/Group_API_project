from custom_user.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Title

from .mixins import ListCreateDestroyViewSet
from .permissions import IsAdmin, IsAdminOrReadOnly, UserPermission
from .serializers import (CategorySerializer, GenreSerializer,
                          GetTokenSerializer, MeSerializer, SignUpSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer)


class GetToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь отсутствует.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if str(data.get('confirmation_code')) == str(user.confirmation_code):
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED
            )
        a = str(data.get('confirmation_code'))
        b = str(user.confirmation_code)
        print(a)
        print(b)
        return Response(
            {'confirmation_code': 'Ошибка кода подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )


class SignUp(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(body=data['email_body'], to=[data['to_email']])
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'email_body': f'{user.username}, {user.confirmation_code}',
            'to_email': user.email,
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

