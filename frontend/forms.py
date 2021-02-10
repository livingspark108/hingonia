from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import *
from apps.student.models import *
from django.forms.models import inlineformset_factory


class StudentUploadContent1(forms.ModelForm):

    class Meta:
        model = StudentUploadContent1
        fields = ['student', 'week', 'challenge', 'challenge_instruction', 'file_1']


class StudentUploadContent2(forms.ModelForm):

    class Meta:
        model = StudentUploadContent1
        fields = ['student', 'week', 'challenge', 'challenge_instruction', 'file_2']
