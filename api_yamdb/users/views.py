from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import AdminOnly
from users.serializers import (
    UserRegistrationSerializer,
    ConfirmationCodeSerializer,
    UserSerializer
)

User = get_user_model()


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
        try:
            email = serializer.initial_data['email']
            username = serializer.initial_data['username']
            user = User.objects.get(email=email, username=username)
            user.confirmation_code = (
                default_token_generator.make_token(user)
            )
            user.save()
        except (User.DoesNotExist, KeyError):
            if serializer.is_valid():
                email = serializer.validated_data['email']
                username = serializer.validated_data['username']
                serializer.save()
                user = get_object_or_404(User, username=username)
                user.confirmation_code = (
                    default_token_generator.make_token(user)
                )
                user.save()
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        send_mail(subject='Код подтверждения Yamdb',
                  message=f'Ваш код подтверждения регистрации: '
                          f'{user.confirmation_code}',
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
            confirmation_code = serializer.validated_data['confirmation_code']
            username = serializer.validated_data['username']
            user = get_object_or_404(User, username=username)
            if confirmation_code == user.confirmation_code:
                user.save()
                token = AccessToken.for_user(user)
                return Response({'token': f'{token}'},
                                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
