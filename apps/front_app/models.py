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
    short_title = models.CharField(max_length=300, blank=False,null=True)
    price = models.FloatField(max_length=300, blank=True,null=True)
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





class Distribution(DateTimeModel):
    title = models.CharField(max_length=300, blank=False)
    date = models.DateField(max_length=2500, null=True, blank=True)
    location = models.CharField(max_length=300, blank=False)
    icon = models.ImageField(upload_to='distribution_icon/',null=True,blank=True)


    def __str__(self):
        return self.title

class DistributionImage(DateTimeModel):
    image = models.ImageField(upload_to='distribution_images/')
    distribution = models.ForeignKey(Distribution, blank=True, null=True, on_delete=models.CASCADE,
                                 related_name='distribution_image')


class Setting(DateTimeModel):
    whatsapp_key = models.CharField(max_length=1000, blank=True,null=True)
