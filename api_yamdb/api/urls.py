from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentsViewSet, GenreViewSet, MeViewSet,
                    RegistrationAPI, ReviewsViewSet, TitleViewSet, UserViewSet,
                    VerifyAccountAPI)

app_name = 'api'


router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet,
                   basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comment'
)


urlpatterns = [
    path('v1/users/me/', MeViewSet.as_view(
        {'patch': 'me',
         'get': 'me'}), name="me_viewset"),
    path('v1/auth/signup/', RegistrationAPI.as_view(), name='signup'),
    path('v1/auth/token/', VerifyAccountAPI.as_view(), name='token'),
    path('v1/', include(router_v1.urls)),
]
