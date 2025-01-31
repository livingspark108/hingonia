from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.urls import reverse

from apps.user.constants import USER_TYPE_CHOICES
from apps.user.models import Subscription

User = get_user_model()


class CreateUserForm(UserCreationForm):
    # type = forms.CharField(widget=forms.HiddenInput(), initial='admin')
    is_staff = forms.BooleanField(widget=forms.HiddenInput(), initial=True)


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'type', 'is_active','is_staff','profile', 'password1', 'password2']


class EditUserForm(UserChangeForm):
    type = forms.CharField(widget=forms.HiddenInput(), initial='admin')
    password_help_text ="Raw passwords are not stored, so there is no way to see this \n user's password, but you can change the password using \n <a href=\"{}\">this form</a>."

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'type', 'is_active','profile', 'password']

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = self.password_help_text.format(reverse('auth-change-password', kwargs={'user_id': self.instance.id}))


class CreateSubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['user', 'plan', 'campaign', 'start_date', 'cow_name', 'razorpay_subscription_id', 'price', 'razorpay_payment_id']