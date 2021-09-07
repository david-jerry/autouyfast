import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Fieldset, Layout, Submit
from django import forms

from .models import CAR_BODY, CAR_DOOR, CAR_MAKE, AutoSearch  # , Stock, Year

CAR_STOCK = (
    ("used", "used"),
    ("new", "new"),
    ("certified", "certified")
)

MILEAGE = (
    (100, "less than 100"),
    (500, "less than 500"),
    (1000, "less than 1000"),
    (2000, "less than 2000"),
    (5000, "less than 5000"),
    (10000, "less than 10000"),
    (50000, "less than 50000"),
    (100000, "less than 100000"),
    (2500000, "less than 250000"),
)
PRICE = (
    (100, "less than 100"),
    (500, "less than 500"),
    (1000, "less than 1000"),
    (2000, "less than 2000"),
    (5000, "less than 5000"),
    (10000, "less than 10000"),
    (50000, "less than 50000"),
    (100000, "less than 100000"),
    (2500000, "less than 250000"),
    (5000000, "less than 500000"),
    (8500000, "less than 850000"),
)
YEAR = (
    (2000, "less than 2000"),
    (2005, "less than 2005"),
    (2010, "less than 2010"),
    (2015, "less than 2015"),
    (2022, "less than 2022"),
)
class CarFilter(django_filters.FilterSet):
    car_mileage = django_filters.ChoiceFilter(empty_label='Mileage', choices=MILEAGE, lookup_expr='lt', widget=forms.Select(attrs={"class":"auto-custom-select"}), label='MILEAGE')
    title = django_filters.ChoiceFilter(empty_label='Make',choices=CAR_MAKE, lookup_expr='icontains', label='MAKE', widget=forms.Select(attrs={"class":"auto-custom-select"}))
    # title = django_filters.CharFilter(lookup_expr='icontains', label='CAR KEYWORD', widget=forms.TextInput(attrs={"class":"a-content"}))
    car_body = django_filters.ChoiceFilter(empty_label='Body',choices=CAR_BODY, lookup_expr='icontains', label='BODY STYLE', widget=forms.Select(attrs={"class":"auto-custom-select"}))
    car_door = django_filters.ChoiceFilter(choices=CAR_DOOR, lookup_expr='icontains', label='DOORS', widget=forms.Select(attrs={"class":"auto-custom-select"}))
    car_price = django_filters.ChoiceFilter(empty_label='Price',choices=PRICE, lookup_expr='lt', widget=forms.Select(attrs={"class":"auto-custom-select"}), label='PRICE')
    car_year = django_filters.ChoiceFilter(empty_label='Year',choices=YEAR, lookup_expr='lt', widget=forms.Select(attrs={"class":"auto-custom-select"}), label='YEAR')
    car_stock = django_filters.ChoiceFilter(empty_label='Used or New',choices=CAR_STOCK, lookup_expr='icontains', widget=forms.Select(attrs={"class":"auto-custom-select"}), label='CONDITION')
    
    class Meta:
        model = AutoSearch
        fields = (
            'car_stock',
            'title',
            'car_year',
            'car_price',
            'car_body',
            'car_door',
            'car_mileage',
        )

class CarSearchFilter(django_filters.FilterSet):
    car_mileage = django_filters.ChoiceFilter(choices=MILEAGE, lookup_expr='lt', widget=forms.Select(attrs={"class":"auto-custom-select"}), label='MILEAGE')
    title = django_filters.ChoiceFilter(choices=CAR_MAKE, lookup_expr='icontains', label='MAKE', widget=forms.Select(attrs={"class":"auto-custom-select"}))
    car_body = django_filters.ChoiceFilter(choices=CAR_BODY, lookup_expr='icontains', label='BODY STYLE', widget=forms.Select(attrs={"class":"auto-custom-select"}))
    car_door = django_filters.ChoiceFilter(choices=CAR_DOOR, lookup_expr='icontains', label='DOORS', widget=forms.Select(attrs={"class":"auto-custom-select"}))
    car_price = django_filters.ChoiceFilter(choices=PRICE, lookup_expr='lt', widget=forms.Select(attrs={"class":"auto-custom-select"}), label='PRICE')
    car_year = django_filters.ChoiceFilter(choices=YEAR, lookup_expr='lt', widget=forms.Select(attrs={"class":"auto-custom-select"}), label='YEAR')
    car_stock = django_filters.ChoiceFilter(choices=CAR_STOCK, lookup_expr='icontains', widget=forms.Select(attrs={"class":"auto-custom-select"}), label='CONDITION')
    
    class Meta:
        model = AutoSearch
        fields = (
            'car_stock',
            'title',
            'car_year',
            'car_price',
            'car_body',
            'car_door',
            'car_mileage',
        )


class HomeSearchFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = AutoSearch
        fields = [
            'title'
            ]
