from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, GenreViewSet, GetToken, SignUp,
                    TitleViewSet, UserViewSet)

router = DefaultRouter()
router.register('categories', CategoriesViewSet,
                basename='category')
router.register('genres', GenreViewSet,
                basename='genres')
router.register('users', UserViewSet,
                basename='users')
router.register('titles',TitleViewSet,
                 basename='titles')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUp.as_view(), name='register'),
    path('v1/auth/token/', GetToken.as_view(), name='token')
]