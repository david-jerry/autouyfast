from django.contrib import admin
from .models import AutoSearch

# Register your models here.
@admin.register(AutoSearch)
class AutoSearchAdmin(admin.ModelAdmin):

    list_display = ["car_title", "car_stock", "car_year"]
    list_filter = ["car_stock", "car_year"]
    search_fields = ["car_title", "car_stock", "car_year"]
    ordering = ['car_title']
    list_per_page = 250