from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import AdminOnly
from users.models import User
from users.serializers import (
    UserRegistrationSerializer,
    ConfirmationCodeSerializer,
    UserSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (AdminOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(data=serializer.data)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save(role=request.user.role)
                return Response(data=serializer.data,
                                status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserSignUpView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        username = serializer.data['username']
        user, _ = User.objects.get_or_create(email=email, username=username)
        confirmation_code = (
            default_token_generator.make_token(user)
        )
        user.save()
        send_mail(subject='Код подтверждения Yamdb',
                  message=f'Ваш код подтверждения регистрации: '
                          f'{confirmation_code}',
                  from_email='yamdb@mail.com',
                  recipient_list=[email],
                  fail_silently=True)
        return Response({'email': email, 'username': username},
                        status=status.HTTP_200_OK)


class TokenObtainView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = serializer.data['confirmation_code']
            username = serializer.data['username']
            user = get_object_or_404(User, username=username)
            if default_token_generator.check_token(user, confirmation_code):
                token = AccessToken.for_user(user)
                return Response({'token': f'{str(token)}'},
                                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
