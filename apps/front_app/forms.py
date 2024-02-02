from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import Select, inlineformset_factory
from django.urls import reverse

from apps.front_app.models import Distribution, DistributionImage

User = get_user_model()


class CreateDistributionForm(forms.ModelForm):

    class Meta:
        model = Distribution
        fields = ['title','date','location']



DistributionImageFormset = inlineformset_factory(Distribution, DistributionImage,
                                          form=CreateDistributionForm,
                                          fields=['image'],
                                          can_delete=True,
                                          extra=1)

class DetailDistributionForm(forms.ModelForm):

    class Meta:
        model = Distribution
        fields = '__all__'


DistributionImageFormset = inlineformset_factory(Distribution, DistributionImage,
                                          form=CreateDistributionForm,
                                          fields=['image'],
                                          can_delete=True,
                                          extra=1)