from .models import AutoSearch
import django_filters


class CarFilter(django_filters.FilterSet):
    class Meta:
        model = AutoSearch
        fields = {
            'car_title': ['icontains'],
            'car_dealer_name': ['icontains'],
            'car_year': ['lt'],
            'car_mileage': ['lt'],
            'car_price': ['lt'],
            'car_stock': ['icontains']
        }