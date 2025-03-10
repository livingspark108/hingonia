from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import *
from django.forms.models import inlineformset_factory



class SetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

class VerifyOTPForm(forms.Form):
    otp = forms.CharField(max_length=6)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    user_id = forms.CharField(widget=forms.HiddenInput)