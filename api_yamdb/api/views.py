from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title
from users.models import User
from users.utils import send_confirmation_code

from .filters import TitlesFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import (AuthorizedOrReadOnly, IsAdminOrReadOnly,
                          IsAdminPermission)
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, MeSerializer,
                          ReadOnlyTitleSerializer, RegistrationSerializer,
                          ReviewsSerializer, TitleSerializer, UserSerializer,
                          VerifyAccountSerializer)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [AuthorizedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [AuthorizedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class RegistrationAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            send_confirmation_code(**serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        username = request.data.get('username')
        email = request.data.get('email')
        if User.objects.filter(username=username, email=email).exists():
            send_confirmation_code(**data)
            return Response(
                {'message': 'Check your email for confirmation code'},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyAccountAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        serializer = VerifyAccountSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data['username']
            confirmation_code = serializer.data['confirmation_code']
            user = get_object_or_404(User, username=username)

            if user.confirmation_code != confirmation_code:
                return Response(
                    {'message': 'Wrong confirmation code'},
                    status=status.HTTP_400_BAD_REQUEST)

            user.save()
            token = RefreshToken.for_user(user)
            return Response(
                {'token': str(token.access_token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MeSerializer
    http_method_names = ['get', 'patch']

    def me(self, request):
        data = request.data
        serializer = MeSerializer(request.user, data=data, partial=True)
        if serializer.is_valid():
            if request.method == 'PATCH':
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminPermission)
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
