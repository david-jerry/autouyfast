from crispy_forms.bootstrap import InlineField, UneditableField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    HTML,
    ButtonHolder,
    Div,
    Field,
    Fieldset,
    Layout,
    Row,
    Submit,
)
from django import forms
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory
from tinymce.widgets import TinyMCE

User = get_user_model()

from .crispy_layout_object import *
from .models import CAR_BODY, CAR_DOOR, CAR_MAKE, AutoSearch, Image, SaveCarSearch


class CarImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['created', 'modified', 'img_url']

CarImageFormset = inlineformset_factory(
    AutoSearch, Image, form=CarImageForm,
    fields=['image'], extra=3, can_delete=True, max_num=20, min_num=1 # can_order=True
)


class AutoSearchForm(forms.ModelForm):

    class Meta:
        model = AutoSearch
        fields = [
            "car_vin",
            "car_stock",
            "car_year",
            "title",
            "car_door",
            "car_body",
            "car_mileage",
            "car_price",
            "car_sub_price",
            "car_transmission",
            "car_ext_color",
            "car_int_color",
            "car_drive_train",
            "car_fuel_type",
            "car_engine",
            "seller_note",
        ]
        widgets = {
            'car_vin': forms.TextInput(attrs={'class':'textinput textInput form-control', 'placeholder': 'Car Vin'}),
            'title': forms.TextInput(attrs={'class':'textinput textInput form-control', 'placeholder': 'Car Name'}),
            'car_price': forms.TextInput(attrs={'class':'textinput textInput form-control', 'placeholder': 'Car Main Price'}),
            'car_sub_price': forms.TextInput(attrs={'class':'textinput textInput form-control', 'placeholder': 'Car Monthly Price'}),
            'car_transmission': forms.TextInput(attrs={'class':'textinput textInput form-control', 'placeholder': 'Car Transmission'}),
            'car_ext_color': forms.TextInput(attrs={'class':'textinput textInput form-control', 'placeholder': 'Car Exterior Color'}),
            'car_int_color': forms.TextInput(attrs={'class':'textinput textInput form-control', 'placeholder': 'Car Interior Color'}),
            'car_drive_train': forms.TextInput(attrs={'class':'textinput textInput form-control', 'placeholder': 'Car Drive Train'}),
            'car_fuel_type': forms.TextInput(attrs={'class':'textinput textInput form-control', 'placeholder': 'Car Fuel Type'}),
            'car_engine': forms.TextInput(attrs={'class':'textinput textInput form-control', 'placeholder': 'Car Engine'}),
            'car_year': forms.Select(attrs={'class':'auto-custom-select', 'placeholder': 'Model Year'}),
            'car_stock': forms.Select(attrs={'class':'auto-custom-select', 'placeholder': 'Used or New'}),
            'car_body': forms.Select(attrs={'class':'auto-custom-select', 'placeholder': 'Used or New'}),
            'car_door': forms.Select(attrs={'class':'auto-custom-select', 'placeholder': 'Used or New'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('title'),
                Field('car_def_image'),
                Field('car_vin'),
                Field('car_stock'),
                Field('car_door'),
                Field('car_body'),
                Field('car_year'),
                Field('car_price'),
                Field('car_sub_price'),
                Field('car_transmission'),
                Field('car_ext_color'),
                Field('car_int_color'),
                Field('car_drive_train'),
                Field('car_fuel_type'),
                Field('car_engine'),
                Field('seller_note'),
                HTML("<br>"),
                Fieldset('Add Car Images',
                    Formset('images')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save', css_class="btn btn-primary btn-block")),
                )
            )


SELLER_CONTACT_REASON = (
    ("Is this still Available", "Availability"),
    ("Do you offer an installmental Payment plan", "Installed Payment"),
)
class ContactCarDealerForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder":"First Name"}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder":"Phone"}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder":"Last Name"}))
    question = forms.ChoiceField(choices=SELLER_CONTACT_REASON)
    message = forms.CharField(widget=TinyMCE(attrs={'cols': 40, 'row': 40, "placeholder":"I will like to know is this car is still available."}))



class SaveCarSearchForm(forms.ModelForm):
    class Meta:
        model = SaveCarSearch
        fields = []
