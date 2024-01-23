from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
from application.custom_model import DateTimeModel


class Mother(DateTimeModel):
    title = models.CharField(max_length=300, blank=False)
    description = models.TextField(max_length=2500, null=True, blank=True)
    mother_image = models.ImageField(upload_to='mother_images', max_length=1000,null=True,blank=True)

class Campaign(DateTimeModel):
    title = models.CharField(max_length=300, blank=False)
    short_description = models.TextField(max_length=2500, null=True, blank=True)
    description = RichTextUploadingField(blank=True, null=True)
    campaign_image = models.ImageField(upload_to='campaign_images', max_length=1000,null=True,blank=True)


class OurTeam(DateTimeModel):
    title = models.CharField(max_length=300, blank=False)
    designation = models.TextField(max_length=200, null=True, blank=True)
    short_description = models.TextField(max_length=2500, null=True, blank=True)
    profile = models.ImageField(upload_to='profile', max_length=1000,null=True,blank=True)

class AboutUs(DateTimeModel):
    title = models.CharField(max_length=1000, blank=False)
    description = models.TextField(max_length=2500, null=True, blank=True)
    banner = models.ImageField(upload_to='banner', max_length=1000,null=True,blank=True)



