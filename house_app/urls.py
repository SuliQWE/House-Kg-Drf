from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import (
    UserProfileListAPIView,
    DetailUserProfileAPIView,
    ListPropertyListAPIView,
    DetailPropertyListAPIView,
    ReviewViewSet,
    ReviewListAPIView,
    RegisterView,
    LogoutView,
    CustomLoginView,
    PricePredict
)

# Роутер для ReviewViewSet
router = routers.SimpleRouter()
router.register(r'review_view', ReviewViewSet, basename='review_view')

urlpatterns = [
    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
    path('review/', ReviewListAPIView.as_view(), name='review_list'),
    path('userprofile/', UserProfileListAPIView.as_view(), name='userprofile_list'),
    path('userprofile/<int:pk>/', DetailUserProfileAPIView.as_view(), name='userprofile_detail'),
    path('property/', ListPropertyListAPIView.as_view(), name='property_list'),
    path('property/<int:pk>/', DetailPropertyListAPIView.as_view(), name='property_detail'),
    path('price/', PricePredict.as_view(), name='predicted_price'),
]
