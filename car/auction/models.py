from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from multiselectfield import MultiSelectField


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('seller', 'seller'),
        ('buyer', 'buyer')
    )
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default='seller')
    phone_number = PhoneNumberField()

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Brand(models.Model):
    brand_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.brand_name


class CarModel(models.Model):
    car_model = models.CharField(max_length=32, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.brand}, {self.car_model}'


class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1980),
                                                        MaxValueValidator(2025)])
    FUEL_TYPE_CHOICES = (
        ('benzin', 'benzin'),
        ('gas', 'gas'),
        ('electro', 'electro'),
        ('disel', 'disel'),
        ('gibrid', 'gibrid')
    )
    fuel_type = MultiSelectField(choices=FUEL_TYPE_CHOICES, max_choices=3)
    TRANSMISSION_CHOICES = (
        ('auto', 'Auto'),
        ('manual', 'Manual')
    )
    transmission = models.CharField(max_length=32, choices=TRANSMISSION_CHOICES)
    mileage = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField()
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.brand}, {self.seller}'


class Auction(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE)
    start_price = models.PositiveIntegerField()
    min_price = models.PositiveIntegerField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    STATUS_CHOICES = (
        ('active', 'active'),
        ('canceled', 'canceled'),
        ('completed', 'completed')
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=32)

    def __str__(self):
        return f'{self.car}, {self.status}'


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.buyer}, {self.auction}, {self.amount}'


class Feedback(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_seller')
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_buyer')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 5)], null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.buyer}, {self.seller}'
