from rest_framework import serializers

from .models import Category, Genre, Title, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей"""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'role',
        )

class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей"""
    class Meta:
        model = Genre
        fields = (
            'name', 'slug'
        )