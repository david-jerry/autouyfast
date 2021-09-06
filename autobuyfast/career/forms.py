from django import forms
from tinymce.widgets import TinyMCE

from .models import CareerApply, EmailSubscribe


class CareerApplyForm(forms.ModelForm):

    class Meta:
        model = CareerApply
        fields = [
            "career",
            "cv",
            "name", 
            "email",
            "nationality",
            "address",
            "linkedin",
            "facebook",
            "twitter"
        ]


