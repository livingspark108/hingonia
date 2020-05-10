import datetime

from django import forms

from .models import User,UserShipping
from django.contrib.auth import get_user_model


class UserShippingForm(forms.ModelForm):
    user = forms.CharField(required=False, label='')
    class Meta:
        model = UserShipping
        fields = ['shipping_email', 'shipping_first_name', 'shipping_last_name', 'shipping_address_1', 'shipping_address_2', 'shipping_zip_code', 'shipping_phone_no', 'shipping_country','shipping_state',
                'shipping_city', 'user']
    def clean_user(self):
        user = self.cleaned_data['user']
        if user == '':
            return None
        else:
            return User.objects.get(id=user)