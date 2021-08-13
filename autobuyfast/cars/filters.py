import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Fieldset, Layout, Submit
from django import forms

from .models import CAR_STOCK, AutoSearch  # , Stock, Year

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
    car_mileage = django_filters.ChoiceFilter(choices=MILEAGE, lookup_expr='lt', widget=forms.Select(attrs={"class":"selectpicker", "data-width":"100%"}), label='Mileage')
    title = django_filters.CharFilter(lookup_expr='icontains', label='Car Name')
    car_dealer_name = django_filters.CharFilter(lookup_expr='icontains', label='Dealer Name')
    car_price = django_filters.ChoiceFilter(choices=PRICE, lookup_expr='lt', widget=forms.Select(attrs={"class":"selectpicker", "data-width":"100%"}), label='Price')
    car_year = django_filters.ChoiceFilter(choices=YEAR, lookup_expr='lt', widget=forms.Select(attrs={"class":"selectpicker", "data-width":"100%"}), label='Manufacturing Year')
    # car_year = django_filters.ModelChoiceFilter(queryset=Year.objects.all(), widget=forms.Select(attrs={"class":"selectpicker", "data-width":"100%"}), label='Manufacturing Year')
    car_stock = django_filters.ChoiceFilter(choices=CAR_STOCK, lookup_expr='lt', widget=forms.Select(attrs={"class":"selectpicker", "data-width":"100%"}), label='Stock Type')
    
    class Meta:
        model = AutoSearch
        fields = (
            'title',
            'car_dealer_name',
            'car_mileage',
            'car_price',
            'car_year',
            'car_stock',
        )
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Fieldset(
    #             'first arg is the legend of the fieldset',
    #             'like_website',
    #             'favorite_number',
    #             'favorite_color',
    #             'favorite_food',
    #             'notes'
    #         ),
    #         ButtonHolder(
    #             Submit('submit', 'Submit', css_class='button white')
    #         )
    #     )

    # def __init__(self, *args, **kwargs):
    #     super(CarFilter, self).__init__(*args, **kwargs)
    #     self.filters['car_mileage'].extra.update(
    #         {
    #             'choices': MILEAGE
    #         })
    #     self.filters['car_price'].extra.update(
    #         {
    #             'choices': PRICE
    #         })

        # filter_overrides = {
        #     models.CharField: {
        #         'filter_class': django_filters.CharFilter,
        #         'extra': lambda f: {
        #             'lookup_expr': 'icontains',
        #         },
        #     },
        #     models.BooleanField: {
        #         'filter_class': django_filters.BooleanFilter,
        #         'extra': lambda f: {
        #             'widget': forms.CheckboxInput,
        #         },
        #     },
        # }
class CarSearchFilter(django_filters.FilterSet):
    car_mileage = django_filters.ChoiceFilter(choices=MILEAGE, lookup_expr='lt', label='Mileage')
    title = django_filters.CharFilter(lookup_expr='icontains', label='Car Name')
    car_dealer_name = django_filters.CharFilter(lookup_expr='icontains', label='Dealer Name')
    car_price = django_filters.ChoiceFilter(choices=PRICE, lookup_expr='lt', label='Price')
    # car_year = django_filters.ChoiceFilter(choices=YEAR, lookup_expr='lt', label='Manufacturing Year')
    car_year = django_filters.ChoiceFilter(choices=YEAR, lookup_expr='lt', label='Manufacturing Year')
    car_stock = django_filters.ChoiceFilter(choices=CAR_STOCK, lookup_expr='lt', label='Stock Type')
    
    class Meta:
        model = AutoSearch
        fields = (
            'title',
            'car_dealer_name',
            'car_mileage',
            'car_price',
            'car_year',
            'car_stock',
        )
