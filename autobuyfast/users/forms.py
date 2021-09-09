from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.db import transaction
from django.forms import widgets
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from autobuyfast.users.models import CarRequest

from .models import AlertSetting, Profile, Testimonial

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_no",
        ]


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_no",
        ]
        widgets = {
            'username': forms.TextInput(attrs={"class":"auto-custom-select mb-3", 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={"class":"auto-custom-select mb-3", 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={"class":"auto-custom-select mb-3", 'placeholder': 'Surname'}),
            'email': forms.EmailInput(attrs={"class":"auto-custom-select mb-3", 'placeholder': 'Email'}),
            'phone_no': forms.TextInput(attrs={"class":"auto-custom-select mb-3", 'placeholder': '+17384758273'}),
            'password1': forms.PasswordInput(attrs={"class":"auto-custom-select mb-3", 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={"class":"auto-custom-select mb-3", 'placeholder': 'Confirm Password'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
    #     self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})
    #     self.fields['last_name'].widget.attrs.update({'placeholder': 'Surname'})
    #     self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
    #     self.fields['phone_no'].widget.attrs.update({'placeholder': '+17384758273'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})


        error_messages = {
            "username": {"unique": _("This username has already been taken.")},
            "email": {"unique": _("This email has already been used.")}
        }



class BuyerForm(forms.ModelForm):
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_seller = False
        user.save()
        return user


class SellerForm(forms.ModelForm):
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_seller = True
        user.save()
        return user


class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profile_display",
            "country",
            "address",
            "city",
            "zipcode",
            "security_quest",
            "security_answer"
        ]


class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profile_display",
            "dealership_name",
            "bio",
            "website",
            "banner_display",
            "country",
            "address",
            "city",
            "zipcode",
            "security_quest",
            "security_answer"
        ]


class TestimonyForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["testimony"]


class AlertSettingsForm(forms.ModelForm):
    class Meta:
        model = AlertSetting
        fields = [
            "newsletter_notif", 
            "car_sold_notif", 
            "car_price_notif"
        ]


class CarRequestForm(forms.ModelForm):
    class Meta:
        model = CarRequest
        fields = [
            'name',
            'email',
            'phone',
            'pickup',
            'services',
            'message',
        ]
        widgets = {
            'pickup': forms.DateInput(attrs={'class': "home-date"}),
        }

    