from django.db import models
from multiselectfield import MultiSelectField

from project.custom_classes import DateUserModel
from .constants import PERMISSIONS_CHOICES


# Create your models here.

class Role(DateUserModel):
    name = models.CharField(unique=True, max_length=25)
    slug = models.CharField(unique=True,null=True, max_length=25)
    permissions = MultiSelectField(choices=PERMISSIONS_CHOICES, blank=True)
    is_active = models.BooleanField('Status', default=True)

    def __str__(self):
        return self.name
