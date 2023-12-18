from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор')
)


class MyUser(AbstractUser):

    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField('Роль', max_length=settings.LIMIT_MIN,
                            choices=CHOICES,
                            default='user')
    confirmation_code = models.CharField(
        max_length=settings.LIMIT_MIN,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('username',)
