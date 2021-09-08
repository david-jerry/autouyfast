from django.urls import path
from django_filters.views import FilterView

from autobuyfast.cars.views import (  # CarLikeFunc,
    CarCreateView,
    CarDeleteView,
    CarSold,
    CarUpdateView,
    CompareCreateView,
    CompareView,
    car_detail_view,
    cars_list_view,
    filter_car_search_view,
    filter_home_car_search_view,
    unwatch_car,
    watch_car,
)

from .filters import CarFilter
from .models import AutoSearch

app_name = "cars"
urlpatterns = [
    path("", view=cars_list_view, name="list"),
    path("create/", view=CarCreateView.as_view(), name="create"),
    path("compare-cars/<slug>/update", view=CompareCreateView.as_view(), name="compare"),
    path("compare-cars/<slug>/", view=CompareView.as_view(), name="compare_detail"),
    path("detail/<slug>/update", view=CarUpdateView.as_view(), name="update"),
    path("detail/<slug>/delete", view=CarDeleteView, name="delete"),
    path("detail/<slug>/sold", view=CarSold, name="sold"),
    path("detail/<slug>/", view=car_detail_view, name="detail"),
    path("search/", view=filter_car_search_view, name="search"),
    path("search/alt/", view=filter_home_car_search_view, name="home_search"),
    path("cars/watch/<slug>/", view=watch_car, name="watch_add"),
    path("cars/unwatch/<slug>/", view=unwatch_car, name="watch_remove"),
]
