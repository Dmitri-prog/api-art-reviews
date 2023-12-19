from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, GenreViewSet, TitleViewSet
from users.views import UserSignUpView, TokenObtainView, UserViewSet
from . import views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', UserSignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenObtainView.as_view(), name='token_obtain'),
]
