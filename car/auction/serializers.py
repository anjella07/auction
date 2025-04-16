from rest_framework import serializers
from .models import *
from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class CustomLoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

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


class UserProfileSimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class BrandListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'brand_name']

class BrandSimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['brand_name']


class CarModelListSerializers(serializers.ModelSerializer):
    brand = BrandSimpleSerializers()
    class Meta:
        model = CarModel
        fields = ['id', 'brand', 'car_model']

class CarModelSimpleSerializers(serializers.ModelSerializer):
    brand = BrandSimpleSerializers()
    class Meta:
        model = CarModel
        fields = ['brand', 'car_model']

class CarListSerializers(serializers.ModelSerializer):
    # car_brand = BrandListSerializers()
    car_model = CarModelSimpleSerializers()
    # seller = UserProfileSimpleSerializers()
    class Meta:
        model = Car
        fields = ['id', 'car_model', 'year', 'price']


class AuctionListSerializers(serializers.ModelSerializer):
    car = CarListSerializers()
    class Meta:
        model = Auction
        fields = ['car', 'min_price', 'end_time', 'status']

class BidSerializers(serializers.ModelSerializer):
    auction = AuctionListSerializers()
    buyer = UserProfileSerializers()
    class Meta:
        model = Bid
        fields = ['auction', 'buyer', 'amount', 'created_at']

class FeedbackSerializers(serializers.ModelSerializer):
    seller = UserProfileSimpleSerializers()
    buyer = UserProfileSimpleSerializers()
    class Meta:
        model = Feedback
        fields = ['seller', 'buyer', 'rating', 'comment', 'created_at']

class BrandDetailSerializers(serializers.ModelSerializer):
    car_brand = CarListSerializers(many=True, read_only=True)
    class Meta:
        model = Brand
        fields = ['brand_name', 'car_brand']

class CarModelDetailSerializers(serializers.ModelSerializer):
    model_car = CarListSerializers(many=True, read_only=True)
    # brand = BrandSimpleSerializers()
    class Meta:
        model = CarModel
        fields = ['model_car']


class CarDetailSerializers(serializers.ModelSerializer):
    car_model = CarModelListSerializers()
    seller = UserProfileSimpleSerializers()
    class Meta:
        model = Car
        fields = ['car_model', 'year', 'car_image', 'fuel_type', 'transmission', 'mileage', 'price', 'description', 'seller']

class AuctionDetailSerializers(serializers.ModelSerializer):
    car = CarListSerializers()
    class Meta:
        model = Auction
        fields = ['car', 'start_price', 'min_price', 'start_time', 'end_time', 'status']

class CarCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class AuctionCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = '__all__'