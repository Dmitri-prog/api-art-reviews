from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.mixins import SerializerMixin

User = get_user_model()


class UserSerializer(SerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'bio', 'role')


class UserRegistrationSerializer(SerializerMixin, serializers.ModelSerializer):

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
