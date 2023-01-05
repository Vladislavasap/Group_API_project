import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

USER_ROLES = [
    ('admin', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('user', 'Администратор'),
]

def user_validation(name):
    if name == 'me':
        raise ValidationError(
            ('Использовать имя <me> в качестве username запрещено.'),
            params={'value': name},
        )

class User(AbstractUser):
    username = models.CharField(
        validators=(user_validation,),
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        verbose_name='about me',
        blank=True
    )
    role = models.CharField(
        max_length=128,
        choices=USER_ROLES,
        default='user',
    )
    confirmation_code = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        null=True,
        blank=True
    )
    password = models.CharField(
        blank=True,
        max_length=128
    )

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
    
    @property
    def is_admin(self):
        return self.role == 'admin'

    class Meta:
        verbose_name = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username
