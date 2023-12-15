from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Данный email уже используется.'
            )
        ]
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
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
        max_length=254,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Данный email уже используется.'
            )
        ]
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
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
        fields = ('email', 'username')

    def validate_username(self, username):
        if username == 'me':
            raise ValidationError(f'Запрещено использовать имя {username}'
                                  f'в качестве username!')
        return username


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
