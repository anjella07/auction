from django_filters import FilterSet
from .models import  Car


class CarFilter(FilterSet):
    class Meta:
        model = Car
        fields = {
            'brand': ['exact'],
            'car_model': ['exact'],
            'year': ['gt', 'lt'],
            'price': ['gt', 'lt'],
            'fuel_type': ['exact'],
            'transmission': ['exact']
        }