from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    """Модель категорий для произведений"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров для произведений"""
    name = models.CharField(max_length=30)
    slug = models.SlugField(
        max_length=30,
        unique=True,
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель конкретного произведения"""
    name = models.CharField(max_length=90)
    year = models.IntegerField()
    description = models.TextField(
        max_length=200,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        default="Жанр не выбран",
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        default="Категория не указана",
        on_delete=models.SET_DEFAULT,
        related_name='titles',
    )