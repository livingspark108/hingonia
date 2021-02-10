from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from apps.user.constants import USER_TYPE_CHOICES


class User(AbstractUser):
    type = models.CharField(choices=USER_TYPE_CHOICES, max_length=20)
    email = models.EmailField(_('email address'), blank=False, unique=True)


