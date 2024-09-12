from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from application.custom_model import DateTimeModel
from apps.front_app.models import CampaignProduct, Campaign
# Create your models here.
from apps.user.constants import USER_TYPE_CHOICES


class User(AbstractUser):
    class Meta:
        app_label = 'user'  # Replace 'user' with the name of your app


    type = models.CharField(choices=USER_TYPE_CHOICES, max_length=20)
    address = models.CharField(null=True,blank=True,max_length=250)
    city = models.CharField(null=True,blank=True,max_length=200)
    pincode = models.CharField(null=True,blank=True,max_length=200)
    email = models.EmailField(_('email address'), blank=True,null=True)
    is_password_save = models.BooleanField(default=False)




class TransactionDetails(DateTimeModel):

    mihpayid = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255, null=True, blank=True)
    mode = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255)
    unmappedstatus = models.CharField(max_length=255)
    campaign_id = models.CharField(max_length=255, null=True, blank=True)

    key = models.CharField(max_length=255)
    txnid = models.CharField(max_length=255)
    amount = models.FloatField(max_length=255)
    cardCategory = models.CharField(max_length=255, null=True, blank=True)
    discount = models.CharField(max_length=255, null=True, blank=True)
    net_amount_debit = models.CharField(max_length=255, null=True, blank=True)
    addedon = models.DateTimeField(null=True, blank=True)
    productinfo = models.CharField(max_length=255, null=True, blank=True)
    firstname = models.CharField(max_length=255, null=True, blank=True)
    lastname = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    pan_number = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    udf1 = models.CharField(max_length=255, null=True, blank=True)
    udf2 = models.CharField(max_length=255, null=True, blank=True)
    udf3 = models.CharField(max_length=255, null=True, blank=True)
    udf4 = models.CharField(max_length=255, null=True, blank=True)
    udf5 = models.CharField(max_length=255, null=True, blank=True)
    udf6 = models.CharField(max_length=255, null=True, blank=True)
    udf7 = models.CharField(max_length=255, null=True, blank=True)
    udf8 = models.CharField(max_length=255, null=True, blank=True)
    udf9 = models.CharField(max_length=255, null=True, blank=True)
    udf10 = models.CharField(max_length=255, null=True, blank=True)
    hash = models.CharField(max_length=255, null=True, blank=True)
    field1 = models.CharField(max_length=255, null=True, blank=True)
    field2 = models.CharField(max_length=255, null=True, blank=True)
    field3 = models.CharField(max_length=255, null=True, blank=True)
    field4 = models.CharField(max_length=255, null=True, blank=True)
    field5 = models.CharField(max_length=255, null=True, blank=True)
    field6 = models.CharField(max_length=255, null=True, blank=True)
    field7 = models.CharField(max_length=255, null=True, blank=True)
    field8 = models.CharField(max_length=255, null=True, blank=True)
    field9 = models.CharField(max_length=255, null=True, blank=True)
    payment_source = models.CharField(max_length=255, null=True, blank=True)
    PG_TYPE = models.CharField(max_length=255, null=True, blank=True)
    bank_ref_num = models.CharField(max_length=255, null=True, blank=True)
    bankcode = models.CharField(max_length=255, null=True, blank=True)
    error = models.CharField(max_length=255, null=True, blank=True)
    error_Message = models.CharField(max_length=255, null=True, blank=True)
    cardnum = models.CharField(max_length=255, null=True, blank=True)
    cardhash = models.CharField(max_length=255, null=True, blank=True)
    issuing_bank = models.CharField(max_length=255, null=True, blank=True)
    card_type = models.CharField(max_length=255, null=True, blank=True)
    is_80g_request = models.BooleanField(default=False)
    is_80g_request_approve = models.BooleanField(default=False)

class ProductItemTrans(DateTimeModel):
    product = models.ForeignKey(CampaignProduct, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=3000, blank=True,null=True)
    tran = models.ForeignKey(TransactionDetails, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.PositiveIntegerField(null=True,blank=True)

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    expiration = models.DateTimeField()





class SubscriptionPlan(models.Model):
    plan_id = models.CharField(max_length=100,unique=True,default=0)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, related_name='subscriptions')
    compaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, related_name='compaign_subscription')
    start_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    razorpay_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     if not self.end_date:
    #         self.end_date = self.start_date + timezone.timedelta(days=self.plan.duration_in_days)
    #     super(Subscription, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} (Active: {self.is_active})"

    # @property
    # def is_expired(self):
    #     return timezone.now() > self.end_date