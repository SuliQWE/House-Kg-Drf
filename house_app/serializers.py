
from rest_framework import serializers
from .models import (Property,PropertyImage,UserProfile,Region,Review,District,City,House)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number', 'user_role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class ListUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name']

class DetailUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class ListPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'title', 'property_type', 'price', 'seller']

class DetailPropertySerializer(serializers.ModelSerializer):
    properties_region = RegionSerializer(many=True, read_only=True)
    properties_city = CitySerializer(many=True, read_only=True)
    properties_district = DistrictSerializer(many=True, read_only=True)
    properties_seller = ListUserProfileSerializer(many=True, read_only=True)
    property_images = PropertyImageSerializer(many=True, read_only=True)
    class Meta:
        model = Property
        fields = '__all__'


class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    created_date=serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    reviews_left = ListUserProfileSerializer()
    reviews_received = ListUserProfileSerializer()
    home_review = ListPropertySerializer()

    class Meta:
        model = Review
        fields = '__all__'

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class HousePredictSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'
