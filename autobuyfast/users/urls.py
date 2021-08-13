from django.urls import path

from autobuyfast.users.views import (
    CarAdListView,
    SavedCars,
    buyer_update_view,
    notification_setting_view,
    seller_update_view,
    testimony_create_view,
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~saved-cars/", view=SavedCars.as_view(), name="watch_list"),
    path("~manage-car-ads/", view=CarAdListView.as_view(), name="ads"),
    path("~update/", view=user_update_view, name="update"),
    path("~update/buyer-profile/", view=buyer_update_view, name="update_buyer"),
    path("~update/seller-profile/", view=seller_update_view, name="update_seller"),
    path("~update/notification-setting/", view=notification_setting_view, name="update_notification"),
    path("~leave/testimony/", view=testimony_create_view, name="create_testimony"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
