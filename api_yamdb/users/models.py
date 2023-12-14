from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор')
)


class MyUser(AbstractUser):

    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField('Роль', max_length=25,
                            choices=CHOICES,
                            default='user')
    confirmation_code = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('username',)
