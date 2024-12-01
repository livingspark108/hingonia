from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import Select, inlineformset_factory
from django.urls import reverse

from apps.front_app.models import Distribution, Campaign, CampaignImage, UploadedFile, \
    HomePageCampaign, Testimonial, Trustee, OurSupporter

User = get_user_model()


class CreateDistributionForm(forms.ModelForm):

    class Meta:
        model = Distribution
        fields = ['title','location','main_image']



class DetailDistributionForm(forms.ModelForm):

    class Meta:
        model = Distribution
        fields = '__all__'


class CreateCampaignForm(forms.ModelForm):

    class Meta:
        model = Campaign
        fields = ['type','mode','is_home', 'title','slug','cow_id','place', 'short_title', 'tag', 'last_date', 'price', 'goal', 'payment_type', 'amt_1', 'amt_2',
                  'amt_3', 'youtube_link', 'short_description','updates', 'description', 'backgroud_type', 'campaign_backgroud',
                  'campaign_image','icon','product']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default value for 'type' and make it non-editable
        self.fields['type'].initial = 'Other'
        self.fields['type'].widget.attrs['readonly'] = True  # Makes the field non-editable

CampaignImageFormset = inlineformset_factory(Campaign, CampaignImage,
                                          form=CreateCampaignForm,
                                          fields=['image'],
                                          can_delete=True,
                                          extra=1)


class UpdateCampaignForm(forms.ModelForm):

    class Meta:
        model = Campaign
        fields = ['type','mode','is_home', 'title','slug','cow_id','place', 'short_title','slug', 'tag', 'last_date', 'price', 'goal', 'payment_type', 'amt_1', 'amt_2',
                  'amt_3', 'youtube_link', 'short_description','updates', 'description', 'backgroud_type', 'campaign_backgroud',
                  'campaign_image','icon','product']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default value for 'type' and make it non-editable
        self.fields['type'].initial = 'Other'
        self.fields['type'].widget.attrs['readonly'] = True  # Makes the field non-editable


class CreateSevaForm(forms.ModelForm):

    class Meta:
        model = Campaign
        fields = ['type','mode','is_home', 'title','slug', 'short_title','slug', 'price',
                  'icon']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default value for 'type' and make it non-editable
        self.fields['type'].initial = 'Seva'
        self.fields['type'].widget.attrs['readonly'] = True  # Makes the field non-editable


SevaImageFormset = inlineformset_factory(Campaign, CampaignImage,
                                          form=CreateSevaForm,
                                          fields=['image'],
                                          can_delete=True,
                                          extra=1)

class UpdateSevaForm(forms.ModelForm):

    class Meta:
        model = Campaign
        fields = ['type','mode','is_home', 'title','slug', 'short_title','slug', 'price',
                  'icon']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default value for 'type' and make it non-editable
        self.fields['type'].initial = 'Seva'
        self.fields['type'].widget.attrs['readonly'] = True  # Makes the field non-editable


class CreateAdoptACawForm(forms.ModelForm):

    class Meta:
        model = Campaign
        fields = ['type','mode','is_home', 'title','slug','cow_id','price', 'goal', 'payment_type', 'short_description', 'description',
                  'campaign_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default value for 'type' and make it non-editable
        self.fields['type'].initial = 'Adopt a cow'
        self.fields['type'].widget.attrs['readonly'] = True  # Makes the field non-editable

AdoptACawImageFormset = inlineformset_factory(Campaign, CampaignImage,
                                          form=CreateAdoptACawForm,
                                          fields=['image'],
                                          can_delete=True,
                                          extra=1)

class UpdateAdoptACawForm(forms.ModelForm):

    class Meta:
        model = Campaign
        fields =  ['type','mode','is_home', 'title','slug','cow_id','price', 'goal', 'payment_type', 'short_description', 'description',
                  'campaign_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default value for 'type' and make it non-editable
        self.fields['type'].initial = 'Adopt a cow'
        self.fields['type'].widget.attrs['readonly'] = True  # Makes the field non-editable

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


class CreateTrusteeForm(forms.ModelForm):

    class Meta:
        model = Trustee
        fields = ['title','designation','type','description','photo']


class CreateOurSupporterForm(forms.ModelForm):

    class Meta:
        model = OurSupporter
        fields = ['title','short_description','description','photo']