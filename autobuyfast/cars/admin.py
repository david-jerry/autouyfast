from django.contrib import admin
from django.utils.safestring import mark_safe

from autobuyfast.utils.export_as_csv import ExportCsvMixin

from .models import AutoSearch, Image, WatchCars  # , Stock, Year


# Register your models here.
class CarImagesInline(admin.StackedInline):
    model = Image

@admin.register(AutoSearch)
class AutoSearchAdmin(admin.ModelAdmin, ExportCsvMixin):
    inlines = [CarImagesInline]
    list_per_page = 250
    actions = [
        "export_as_csv",
    ]
    list_display = [
        'dealer',
        'car_vin',
        'car_stock',
        'car_year',
        'title',
        'slug',
        'car_url',
        'car_mileage',
        'car_price',
        'car_history',
        'car_dealer_name',
        'car_dealer_phone',
        'car_transmission',
        'car_ext_color',
        'car_int_color',
        'car_drive_train',
        'car_fuel_type',
        'car_engine',
        'seller_note',
    ]
    list_filter = ["car_stock", "car_year"]
    search_fields = ["title", "car_stock", "car_year"]
    ordering = ['title']
    list_per_page = 250

    class Meta:
        model = AutoSearch

    def image(self, obj):
        return mark_safe(
            '<img src="{url}" width="120px" height="auto" />'.format(
                url=obj.image.image.url,
            )
        )

    def save_model(self, request, obj, form, change):
        if change:
            obj.dealer = request.user
        super().save_model(request, obj, form, change)


admin.site.register(WatchCars)
# admin.site.register(Stock)
