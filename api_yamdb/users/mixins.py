from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class SerializerMixin(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        max_length=settings.LIMIT_MAX,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Данный email уже используется.'
            )
        ]
    )
    username = serializers.CharField(
        required=True,
        max_length=settings.LIMIT_MED,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=('Данное username уже используется, '
                         'придумайте другое username.')
            ),
            RegexValidator(
                r'^[\w.@+-]+$'
            )
        ]
    )
