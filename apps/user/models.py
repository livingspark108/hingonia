from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from application.custom_model import DateTimeModel
# Create your models here.
from apps.user.constants import USER_TYPE_CHOICES


class User(AbstractUser):
    type = models.CharField(choices=USER_TYPE_CHOICES, max_length=20)
    address = models.CharField(null=True,blank=True,max_length=250)
    city = models.CharField(null=True,blank=True,max_length=200)
    pincode = models.CharField(null=True,blank=True,max_length=200)
    email = models.EmailField(_('email address'), blank=True,null=True)
    is_password_save = models.BooleanField(default=False)



class TransactionDetails(DateTimeModel):

    mihpayid = models.CharField(max_length=255)
    mode = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255)
    unmappedstatus = models.CharField(max_length=255)
    promoter_no = models.CharField(max_length=255, null=True, blank=True)
    campaign_id = models.CharField(max_length=255, null=True, blank=True)
    key = models.CharField(max_length=255)
    txnid = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
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


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    expiration = models.DateTimeField()