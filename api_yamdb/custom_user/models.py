from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Создаю кастомного юзера с ролями"""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=12,
        choices=ROLE_CHOICES,
        default=USER
    )
    
    def __str__(self):
        return f'{self.username}'