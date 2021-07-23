from django.urls import path
from django_filters.views import FilterView
from .filters import CarFilter
from .models import AutoSearch

from autobuyfast.cars.views import (
    cars_list_view,
    filter_car_search_view,
)

app_name = "cars"
urlpatterns = [
    path("", view=cars_list_view, name="list"),
    path("search/", view=filter_car_search_view, name="search"),
]
