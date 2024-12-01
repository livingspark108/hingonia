from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify

from application.settings.common import AUTH_USER_MODEL
# Create your models here.
from application.custom_model import DateTimeModel
from apps.front_app.constants import *

class Mother(DateTimeModel):
    title = models.CharField(max_length=300, blank=False)
    description = models.TextField(max_length=2500, null=True, blank=True)
    mother_image = models.ImageField(upload_to='mother_images', max_length=1000,null=True,blank=True)

    title_hindi = models.CharField(max_length=300, blank=False, null=True)
    description_hindi = models.TextField(max_length=2500, null=True, blank=True)


class CampaignProduct(DateTimeModel):
    title = models.CharField(max_length=3000, blank=False)
    image = models.ImageField(upload_to='product_image', max_length=1000,null=True,blank=True)
    unit_title = models.CharField(max_length=3000, blank=False)
    goal = models.FloatField(max_length=300, blank=False)
    price = models.FloatField(max_length=300, blank=False)

    def __str__(self):
        return self.title


class Testimonial(DateTimeModel):
    title = models.CharField(max_length=3000, blank=False)
    designation = models.CharField(max_length=3000, blank=False)
    description = models.CharField(max_length=3000, blank=False)
    photo = models.ImageField(null=True)
    def __str__(self):
        return self.title


class Trustee(DateTimeModel):
    title = models.CharField(max_length=3000, blank=False)
    designation = models.CharField(max_length=3000, blank=False)
    description = models.CharField(max_length=3000, blank=False)
    order_number = models.IntegerField(max_length=3000, blank=True,null=True)
    type = models.CharField(choices=TRUSTEE_CHOICE,max_length=200, blank=False,default='Trustee')
    photo = models.ImageField(null=True)
    def __str__(self):
        return self.title


class OurSupporter(DateTimeModel):
    title = models.CharField(max_length=3000, blank=False)
    short_description = models.CharField(max_length=3000, blank=False,null=True)
    description = RichTextField(max_length=3000, blank=False,null=True)
    photo = models.ImageField(null=True)
    def __str__(self):
        return self.title


class Campaign(DateTimeModel):
    title = models.CharField(max_length=300, blank=False)
    slug = models.SlugField(unique=True,max_length=300, blank=False,null=True)
    short_title = models.CharField(max_length=300, blank=False,null=True)
    place = models.CharField(max_length=300, blank=False,null=True)
    tag = models.CharField(max_length=1000, blank=False,null=True)
    cow_id = models.CharField(max_length=1000, blank=True,null=True)
    price = models.FloatField(max_length=300, blank=False,null=True)
    goal = models.FloatField(max_length=300, blank=True,null=True)
    favourite = models.BooleanField(default=False)
    is_home = models.BooleanField(default=False)
    last_date = models.DateTimeField(max_length=300, blank=True,null=True)


    short_description = models.TextField(max_length=2500, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    updates = RichTextField(null=True, blank=True)

    youtube_link = models.CharField(max_length=300, blank=True,null=True)

    payment_type = models.CharField(choices=PAYMENT_TYPE,max_length=300, blank=False,null=True,default='One Time')
    mode = models.CharField(choices=MODE_TYPE,max_length=300, blank=False,null=True,default='Both Monthly and One Time')

    type = models.CharField(choices=CAMPAIGN_TYPE,max_length=300, blank=False,null=True,default='Other')
    amt_1 = models.IntegerField(blank=True,null=True)
    amt_2 = models.IntegerField(blank=True,null=True)
    amt_3 = models.IntegerField(blank=True,null=True)
    backgroud_type = models.CharField(choices=BG_TYPE_CHOICES,max_length=300, blank=False,null=True,default='red')
    campaign_image = models.ImageField(upload_to='campaign_images', max_length=1000,null=True,blank=True)
    campaign_backgroud = models.ImageField(upload_to='campaign_backgroud',null=True,blank=True)
    product = models.ManyToManyField(CampaignProduct,blank=True)
    def save(self, *args, **kwargs):
        # Generate slug from title without spaces
        if self.pk:
            self.slug = self.slug
        else:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)



    def __str__(self):
        return self.title


class AdoptedCow(DateTimeModel):
    user = models.ForeignKey(
        AUTH_USER_MODEL,  # Use the custom user model defined in settings
        on_delete=models.CASCADE,
        related_name='adopted_cows_user',  # Changed to make the related name more descriptive
        null=True,
        blank=False
    )
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='adopted_campaign', null=True, blank=False)

class Product(DateTimeModel):
    title = models.CharField(max_length=300, blank=False)
    slug = models.SlugField(unique=True,max_length=300, blank=False,null=True)
    price = models.FloatField(max_length=300, blank=True,null=True)
    image = models.ImageField(upload_to='product_image', max_length=1000,null=True,blank=True)
    short_description = models.TextField(max_length=2500, null=True, blank=True)
    description = models.TextField(max_length=2500, null=True, blank=True)

    def __str__(self):
        return self.title

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

    location = models.CharField(max_length=300, blank=True,null=True)
    main_image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.title

class DistributionImage(DateTimeModel):
    image = models.ImageField(upload_to='distribution_images/')
    distribution = models.ForeignKey(Distribution, blank=True, null=True, on_delete=models.CASCADE,
                                 related_name='distribution_image')

class CampaignImage(DateTimeModel):
    image = models.ImageField(upload_to='campaign_images/')
    campaign = models.ForeignKey(Campaign, blank=True, null=True, on_delete=models.CASCADE,
                                 related_name='campaign_multiple_image')

class Setting(DateTimeModel):
    whatsapp_key = models.CharField(max_length=1000, blank=True,null=True)
    admin_email = models.CharField(max_length=1000, blank=True,null=True)
    header_script = models.TextField(blank=True,null=True)
    csr_certificate = models.FileField(blank=True,null=True)
    three_years_report = models.FileField(blank=True,null=True)
    twelve_a_skbt = models.FileField('12 A - SKBT',blank=True,null=True)
    eighty_g_skbt = models.FileField('80 G - SKBT',blank=True,null=True)
    fcra_registration_certificate = models.FileField('FCRA - Registration Certificate',blank=True,null=True)
    thankyou_page_script = models.TextField(blank=True,null=True)
    min_order_value = models.IntegerField(blank=False,null=True)


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=50, blank=True,null=True)
    uploader_id = models.CharField(max_length=100, blank=True,null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class Gallery(DateTimeModel):
    title = models.CharField(max_length=300, blank=False)
    location = models.CharField(max_length=300, blank=True,null=True)

class HomeIcon(DateTimeModel):
    title = models.CharField(max_length=300, blank=True, null=True)
    amount = models.CharField(max_length=300, blank=True, null=True)
    icon = models.ImageField(max_length=300, blank=True, null=True)

class HomeSlider(DateTimeModel):
    title = models.CharField(max_length=300, blank=True, null=True)
    type = models.CharField(choices=SLIDER_TYPE,max_length=300, blank=True, null=True)
    amount = models.CharField(max_length=300, blank=True, null=True)
    icon = models.ImageField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    main_image = models.ImageField(max_length=300, blank=True, null=True)


class HomePageCampaign(DateTimeModel):
    campaign_1 = models.ForeignKey(Campaign, blank=True, null=True, on_delete=models.CASCADE,
                                 related_name='campaign_setting_1')
    campaign_2 = models.ForeignKey(Campaign, blank=True, null=True, on_delete=models.CASCADE,
                                   related_name='campaign_setting_2')
    campaign_3 = models.ForeignKey(Campaign, blank=True, null=True, on_delete=models.CASCADE,
                                   related_name='campaign_setting_3')
    campaign_4 = models.ForeignKey(Campaign, blank=True, null=True, on_delete=models.CASCADE,
                                   related_name='campaign_setting_4')
    campaign_5 = models.ForeignKey(Campaign, blank=True, null=True, on_delete=models.CASCADE,
                                   related_name='campaign_setting_5')
    campaign_6 = models.ForeignKey(Campaign, blank=True, null=True, on_delete=models.CASCADE,
                                   related_name='campaign_setting_6')


class HomePageContent(DateTimeModel):
    youtube_link = models.CharField(max_length=300, blank=True, null=True)
    first_title = models.CharField("1 Title",max_length=300, blank=True, null=True)
    first_icon = models.ImageField("1 Icon",max_length=300, blank=True, null=True)
    first_number = models.CharField("1 Number",max_length=300, blank=True, null=True)
    second_title = models.CharField("2 Title",max_length=300, blank=True, null=True)
    second_icon = models.ImageField("2 Icon",max_length=300, blank=True, null=True)
    second_number = models.CharField("2 Number",max_length=300, blank=True, null=True)
    third_title = models.CharField("3 Title",max_length=300, blank=True, null=True)
    third_icon = models.ImageField("3 Icon",max_length=300, blank=True, null=True)
    third_number = models.CharField("3 Number",max_length=300, blank=True, null=True)
    fourth_title = models.CharField("4 Title",max_length=300, blank=True, null=True)
    fourth_icon = models.ImageField("4 Icon",max_length=300, blank=True, null=True)
    fourth_number = models.CharField("4 Number",max_length=300, blank=True, null=True)
    five_title = models.CharField("5 Title",max_length=300, blank=True, null=True)
    five_icon = models.ImageField("5 Icon",max_length=300, blank=True, null=True)
    five_number = models.CharField("5 Number",max_length=300, blank=True, null=True)
    six_title = models.CharField("6 Title",max_length=300, blank=True, null=True)
    six_icon = models.ImageField("6 Icon",max_length=300, blank=True, null=True)
    six_number = models.CharField("6 Number",max_length=300, blank=True, null=True)



class Order(DateTimeModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order_date = models.DateTimeField(auto_now_add=True)
    product_name = models.CharField(max_length=255,blank=True, null=True)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE,
                                   related_name='order_product')
    address = models.CharField(max_length=255,blank=True, null=True)
    comment = models.CharField(max_length=255,blank=True, null=True)
    first_name = models.CharField(max_length=255,blank=True, null=True)
    last_name = models.CharField(max_length=255,blank=True, null=True)
    email = models.CharField(max_length=255,blank=True, null=True)
    phone = models.CharField(max_length=255,blank=True, null=True)
    country = models.CharField(max_length=255,blank=True, null=True)
    pincode = models.CharField(max_length=255,blank=True, null=True)
    state = models.CharField(max_length=255,blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id} by {self.customer.username}'
