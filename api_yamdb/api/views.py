import datetime

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import (DjangoFilterBackend,
                                           CharFilter, FilterSet)

from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Category, Genre, Review, Title
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializerCreateAndUpdate, TitleSerializerGet)
from .permissions import IsAdminOrReadOnly


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ['name', 'year', ]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'destroy']:
            return TitleSerializerCreateAndUpdate
        return TitleSerializerGet


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter,)
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        pub_date = datetime.datetime.now()
        serializer.save(author=self.request.user, pub_date=pub_date)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        pub_date = datetime.datetime.now()
        serializer.save(author=self.request.user, review=review,
                        pub_date=pub_date)
