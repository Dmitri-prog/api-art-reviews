from datetime import datetime

from django import forms
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializerCreateAndUpdate(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = datetime.now().year
        if not value <= year:
            raise serializers.ValidationError('Проверьте год произведения')
        return value


class TitleSerializerGet(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=False)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        rating = Review.objects.filter(title=obj.id).aggregate(Avg('score'))
        return rating['score__avg']


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    def validate(self, data):

        if self.context.get('request').method == 'POST':
            if Review.objects.filter(author=self.context.get('request').user,
                                     title=self.context.
                                     get('view'
                                         ).kwargs.get('title_id')).exists():
                raise forms.ValidationError(
                    'Этот пользователь уже оставлял отзыв!')
        return data

    class Meta:
        fields = '__all__'
        read_only_fields = ('title', 'id', 'pub_date',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        read_only_fields = ('review', 'id', 'pub_date',)
        model = Comment
