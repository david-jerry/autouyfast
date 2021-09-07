from django import forms
from tinymce.widgets import TinyMCE

from .models import EmailSubscribe


class EmailSubscribeForm(forms.ModelForm):
    class Meta:
        model = EmailSubscribe
        fields = ['email']


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder": "Your Email"}))
    subject = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Why are your mailing us?"}))
    message = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'row': 40}))
