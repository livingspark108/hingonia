from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import Select, inlineformset_factory
from django.urls import reverse

from apps.front_app.models import Distribution, DistributionImage, Campaign, CampaignImage, UploadedFile, \
    HomePageCampaign, Testimonial

User = get_user_model()


class CreateDistributionForm(forms.ModelForm):

    class Meta:
        model = Distribution
        fields = ['title','location','main_image','youtube_1','youtube_2','youtube_3','youtube_4']



class DetailDistributionForm(forms.ModelForm):

    class Meta:
        model = Distribution
        fields = '__all__'


class CreateCampaignForm(forms.ModelForm):

    class Meta:
        model = Campaign
        fields = ['type','mode','is_home', 'title','slug','place', 'short_title', 'tag', 'last_date', 'price', 'goal', 'payment_type', 'amt_1', 'amt_2',
                  'amt_3', 'youtube_link', 'short_description','updates', 'description', 'backgroud_type', 'campaign_backgroud',
                  'campaign_image','product']


CampaignImageFormset = inlineformset_factory(Campaign, CampaignImage,
                                          form=CreateCampaignForm,
                                          fields=['image'],
                                          can_delete=True,
                                          extra=1)

class UpdateCampaignForm(forms.ModelForm):

    class Meta:
        model = Campaign
        fields = ['type','mode','is_home', 'title','slug','place', 'short_title','slug', 'tag', 'last_date', 'price', 'goal', 'payment_type', 'amt_1', 'amt_2',
                  'amt_3', 'youtube_link', 'short_description','updates', 'description', 'backgroud_type', 'campaign_backgroud',
                  'campaign_image','product']

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

class HomePageCampaignForm(forms.ModelForm):
    class Meta:
        model = HomePageCampaign
        fields = ['campaign_1','campaign_2','campaign_3','campaign_4','campaign_5','campaign_6']


class CreateTestimonialForm(forms.ModelForm):

    class Meta:
        model = Testimonial
        fields = ['title','designation','description','photo']