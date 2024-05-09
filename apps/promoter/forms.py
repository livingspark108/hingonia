from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import Select
from django.urls import reverse

from .models import *

User = get_user_model()


class CreatePromoterForm(forms.ModelForm):

    class Meta:
        model = Promoter
        fields = ['mobile_no']


class EditPromoterForm(forms.ModelForm):

    class Meta:
        model = Promoter
        fields = ['mobile_no']


class CreatePromoterUserForm(UserCreationForm):
    type = forms.CharField(widget=forms.HiddenInput(), initial='promoter')
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'type', 'is_active', 'password1', 'password2']
        # fields = ['username', 'email', 'type', 'is_active', 'password1', 'password2']


class EditPromoterUserForm(UserChangeForm):
    type = forms.CharField(widget=forms.HiddenInput(), initial='promoter')
    email = forms.EmailField(required=True)
    password_help_text ="Raw passwords are not stored, so there is no way to see this \n user's password, but you can change the password using \n <a href=\"{}\">this form</a>."

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'type', 'is_active']
        # fields = ['username', 'email', 'type', 'is_active', 'password']

    def __init__(self, *args, **kwargs):
        super(EditPromoterUserForm, self).__init__(*args, **kwargs)
        self.fields.pop('password', None)

