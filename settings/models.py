from django.db import models
from project.custom_classes import DateUserModel
# Create your models here.


class Country(DateUserModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class State(DateUserModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10,blank=True, null=True)

    def __str__(self):
        return self.name


class StateList(DateUserModel):
    name = models.CharField(max_length=50,blank=True,null=True)
    country_code = models.CharField(max_length=50,null=True)