from django.conf import settings
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'bio', 'role')


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        max_length=settings.LIMIT_MAX,
    )
    username = serializers.CharField(
        required=True,
        max_length=settings.LIMIT_MED,
        validators=[
            RegexValidator(
                r'^[\w.@+-]+$'
            )
        ]
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        username = data['username']
        email = data['email']
        if username.lower() == 'me':
            raise ValidationError(f'Запрещено использовать имя {username}'
                                  f'в качестве username!')
        elif (User.objects.filter(username=username).exists()
                and not User.objects.filter(email=email).exists()):
            raise serializers.ValidationError(
                'Данное username уже используется, '
                'придумайте другое username.')
        elif (User.objects.filter(email=email).exists()
                and not User.objects.filter(username=username).exists()):
            raise serializers.ValidationError(
                'Данный email уже используется.')
        return data


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
