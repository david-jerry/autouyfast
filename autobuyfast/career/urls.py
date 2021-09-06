from django.urls import path

from autobuyfast.career.views import career_detail_view, career_view

app_name = "careers"
urlpatterns = [
    path('', career_view, name='list'),
    path('<slug>/', career_detail_view, name='detail'),
]
