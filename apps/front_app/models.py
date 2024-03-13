from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

# Create your models here.
from application.custom_model import DateTimeModel
from apps.front_app.constants import BG_TYPE_CHOICES


class Mother(DateTimeModel):
    title = models.CharField(max_length=300, blank=False)
    description = models.TextField(max_length=2500, null=True, blank=True)
    mother_image = models.ImageField(upload_to='mother_images', max_length=1000,null=True,blank=True)

    title_hindi = models.CharField(max_length=300, blank=False, null=True)
    description_hindi = models.TextField(max_length=2500, null=True, blank=True)

class Campaign(DateTimeModel):
    title = models.CharField(max_length=300, blank=False)
    slug = models.SlugField(unique=True,max_length=300, blank=False,null=True)
    short_title = models.CharField(max_length=300, blank=False,null=True)
    price = models.FloatField(max_length=300, blank=True,null=True)
    short_description = models.TextField(max_length=2500, null=True, blank=True)
    description = RichTextUploadingField(blank=True, null=True)
    amt_1 = models.IntegerField(max_length=300, blank=True,null=True)
    amt_2 = models.IntegerField(max_length=300, blank=True,null=True)
    amt_3 = models.IntegerField(max_length=300, blank=True,null=True)
    backgroud_type = models.CharField(choices=BG_TYPE_CHOICES,max_length=300, blank=False,null=True,default='red')
    campaign_image = models.ImageField(upload_to='campaign_images', max_length=1000,null=True,blank=True)
    campaign_backgroud = models.ImageField(upload_to='campaign_backgroud', max_length=1000,null=True,blank=True)

    def save(self, *args, **kwargs):
        # Generate slug from title without spaces
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def save_base(self, *args, **kwargs):
        # Generate slug from title without spaces if the title has changed

        self.slug = slugify(self.title)

        super().save_base(*args, **kwargs)
class OurTeam(DateTimeModel):
    title = models.CharField(max_length=300, blank=False)
    designation = models.TextField(max_length=200, null=True, blank=True)
    short_description = models.TextField(max_length=2500, null=True, blank=True)
    profile = models.ImageField(upload_to='profile', max_length=1000,null=True,blank=True)

class AboutUs(DateTimeModel):
    title = models.CharField(max_length=1000, blank=False)
    description = models.TextField(max_length=2500, null=True, blank=True)
    banner = models.ImageField(upload_to='banner', max_length=1000,null=True,blank=True)


class AbandonCart(DateTimeModel):
    mobile_no = models.CharField(max_length=1000, blank=False,null=True)
    email = models.CharField(max_length=1000, blank=False,null=True)
    full_name = models.CharField(max_length=1000, blank=False,null=True)





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
    admin_email = models.CharField(max_length=1000, blank=True,null=True)
    min_order_value = models.IntegerField(blank=False,null=True)

