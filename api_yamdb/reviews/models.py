from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


class Genre(models.Model):

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    year = models.IntegerField(
        verbose_name='Год выпуска'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)],
        verbose_name='Оценка'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Время добавления',
        null=True
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=['author', 'title'],
                                               name='ReteatedReview')]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Время добавления',
        null=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    TEXT_LIMIT = 20

    def __str__(self):
        return self.text[:self.TEXT_LIMIT]
