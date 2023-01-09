from custom_user.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей чтобы с ними работал админ"""
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(required=True, max_length=150,
    validators=[UnicodeUsernameValidator(),])
    class Meta:
        model = User
        fields = (
            'username', 'email', 'bio', 'first_name',
            'last_name', 'role',
        )


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей чтобы запросить
       данные о себе или поменять их"""
    last_name = serializers.CharField(max_length=150)
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )
        read_only_fields = ('role',) # чтобы пользователь не поменял себе роль


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров"""
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений(чтение)"""
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description',
            'genre', 'category'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для  произведений(запись)"""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        read_only = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only = ('id',)


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания отзывов"""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,)
    score = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only = ('id',)

    def validate(self, data):
        request = self.context.get('request')
        title = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(author=request.user, title=title).exists():
            raise serializers.ValidationError('Your review on this title is '
                                              'already exists')
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с отзывами"""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,)
    score = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only = ('id',)