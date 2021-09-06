from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from autobuyfast.utils.export_as_csv import ExportCsvMixin

from .forms import (
    BuyerForm,
    BuyerProfileForm,
    SellerForm,
    SellerProfileForm,
    TestimonyForm,
    UserChangeForm,
    UserCreationForm,
)
from .models import AlertSetting, CarRequest, Profile, Testimonial

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin, ExportCsvMixin):

    form = UserChangeForm
    add_form = UserCreationForm
    list_per_page = 250
    empty_value_display = "-empty-"
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "phone_no")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "has_testified",
                    "is_seller",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = [
        "username",
        "first_name",
        "last_name",
        "phone_no",
        "has_testified",
        "is_seller",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    list_editable = [
        "first_name",
        "last_name",
        "phone_no",
        "has_testified",
        "is_seller",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    search_fields = [
        "first_name",
        "last_name",
        "phone_no",
    ]
    actions = [
        "export_as_csv",
    ]


class TestimonialAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Testimonial
    list_per_page = 250
    empty_value_display = "-empty-"
    list_display = ["__str__", "testimony", "active"]
    list_editable = ["testimony", "active"]
    search_fields = ["testimony", "active"]
    actions = [
        "export_as_csv",
    ]


admin.site.register(Testimonial, TestimonialAdmin)

admin.site.register(CarRequest)


class ProfileAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Profile
    list_per_page = 250
    empty_value_display = "-empty-"
    fieldsets = (
        (None, {"fields": ("user",)}),
        (
            _("Dealer Info"),
            {"fields": ("dealership_name", "bio", "website", "banner_display")},
        ),
        (
            _("General Profile Info"),
            {
                "fields": (
                    "profile_display",
                    "country",
                    "address",
                    "city",
                    "zipcode",
                    "security_quest",
                    "security_answer",
                )
            },
        ),
    )
    list_display = ["user", "bio", "website", "banner_display"]
    list_editable = ["bio", "website", "banner_display"]
    search_fields = ["user", "bio", "website", "banner_display"]
    actions = [
        "export_as_csv",
    ]


admin.site.register(Profile, ProfileAdmin)
