from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

CHOICES = (
    (USER, 'пользователь'),
    (MODERATOR, 'модератор'),
    (ADMIN, 'администратор')
)


class User(AbstractUser):

    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField('Роль', max_length=settings.LIMIT_MIN,
                            choices=CHOICES,
                            default=USER)

    class Meta:
        ordering = ('username',)
