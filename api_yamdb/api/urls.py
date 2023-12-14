from django.urls import include, path
from rest_framework import routers

from users.views import UserSignUpView, TokenObtainView, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', UserSignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenObtainView.as_view(), name='token_obtain'),
]
