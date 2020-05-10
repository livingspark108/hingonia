from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django_countries.fields import CountryField

from project.custom_classes import DateUserModel
from .constants import *
from settings import models as setting_model


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class User(AbstractUser):
    first_name = models.CharField('First name', max_length=128, blank=True, null=True)
    last_name = models.CharField('Last name', max_length=128, blank=True, null=True)
    email = models.EmailField('Email Address', blank=False, null=False, unique=True)
    phone_no = models.CharField('Phone number', max_length=128, blank=False, null=True, unique=True, validators=[
        RegexValidator(
            regex=r'[0-9]',
            message='Invalid phone number',
            code='invalid_phone_no'
        ),
    ])
    address_1 = models.CharField('Address 1', max_length=128, blank=True, null=True)
    address_2 = models.CharField('Address 2', max_length=128, blank=True, null=True)
    city = models.CharField('City', max_length=128, blank=True, null=True)
    zip_code = models.CharField('Zip code', max_length=128, blank=True, null=True)
    country = CountryField(null=True)
    state = models.ForeignKey(setting_model.State, on_delete=models.SET_NULL, blank=True,
                              null=True)
    role = models.CharField('Role', choices=CHOICES, max_length=100, null=True, blank=True)
    is_email_verified = models.BooleanField('Email verified', default=False)
    is_phone_no_verified = models.BooleanField('Phone verified', default=False)
    image = models.ImageField(upload_to='avatar/', blank=True, null=True)