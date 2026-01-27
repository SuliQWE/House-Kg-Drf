from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    ListUserProfileSerializer,
    DetailUserProfileSerializer,
    ListPropertySerializer,
    DetailPropertySerializer,
    ReviewSerializer,
    ReviewCreateSerializer,
    UserSerializer,
    LoginSerializer,
    PropertyCreateSerializer
)
from .models import UserProfile, Property, Review
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PropertyFilter
from .pagination import PropertyPagination
from .permission import CreatePropertyPermission, CreateReviewPermission


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIView(generics.ListAPIView):
    serializer_class = ListUserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.all()



class DetailUserProfileAPIView(generics.RetrieveAPIView):
    serializer_class = DetailUserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.all()


class ListPropertyListAPIView(generics.ListAPIView):
    serializer_class = ListPropertySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['title']
    ordering_fields = ['price', 'created_date', 'area']
    pagination_class = PropertyPagination

    def get_queryset(self):
        return Property.objects.all()


class DetailPropertyListAPIView(generics.RetrieveAPIView):
    serializer_class = DetailPropertySerializer

    def get_queryset(self):
        return Property.objects.all()

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertyCreateSerializer
    permission_classes = [CreatePropertyPermission]

    def get_queryset(self):
        return Property.objects.filter(seller=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewCreateSerializer

    def get_queryset(self):
        return Review.objects.filter(reviews_left=self.request.user.id)


class ReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # Показываем все отзывы
        return Review.objects.all()
