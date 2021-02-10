from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import *
from django.forms.models import inlineformset_factory


class TeacherDashboardForm(forms.ModelForm):

    class Meta:
        model = TeacherDashboard
        fields = ['title', 'description']


class SupervisorDashboardForm(forms.ModelForm):

    class Meta:
        model = SupervisorDashboard
        fields = ['title', 'description']


class GuideDashboardForm(forms.ModelForm):

    class Meta:
        model = GuideDashboard
        fields = ['title', 'description']
