from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Div, Row, HTML, ButtonHolder, Submit
from crispy_forms.bootstrap import InlineField, UneditableField

User = get_user_model()

from .models import AutoSearch, CAR_BODY, CAR_DOOR, CAR_MAKE

class AutoSearchForm(forms.Form):
    car_make = forms.ChoiceField(initial="all", choices=CAR_MAKE)
    car_door = forms.ChoiceField(choices=CAR_DOOR)
    car_body = forms.ChoiceField(choices=CAR_BODY)
    zipcode = forms.CharField(initial='00674')
    min_year = forms.IntegerField(initial='1991')
    max_year = forms.IntegerField(initial='2021')
    max_mileage = forms.IntegerField(initial='150000')
    min_price = forms.IntegerField(initial='1000')
    max_price = forms.IntegerField(initial='250000')

