from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from application.custom_model import DateTimeModel
from application.email_helper import send_welcome_user
from apps.front_app.models import CampaignProduct, Campaign
# Create your models here.
from apps.user.constants import USER_TYPE_CHOICES
from django.test import RequestFactory
from django.db.models.query import QuerySet

class SoftDeletionUserQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionUserQuerySet, self).update(is_deleted=True)

    def delete_hard(self):
        return super(SoftDeletionUserQuerySet, self).delete()

    def alive(self):
        return self.filter(is_deleted=False)

    def dead(self):
        return self.filter(is_deleted=True)


class SoftDeleteUserManager(BaseUserManager):
    def __init__(self, *args, **kwargs):
        self.with_deleted = kwargs.pop('deleted', None)
        super(SoftDeleteUserManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.with_deleted:
            return SoftDeletionUserQuerySet(self.model)
        return SoftDeletionUserQuerySet(self.model).filter(is_deleted=False)

    def delete_hard(self):
        return self.get_queryset().hard_delete()

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email,username, password, **extra_fields):

        print("her here her")
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

    def save(self, *args, **kwargs):
        # Check if the user is new (i.e., doesn't have a primary key yet)
        is_new_user = self.pk is None

        super().save(*args, **kwargs)  # Call the original save method to ensure the user is saved first

        # Only send the email if this is a new user
        if is_new_user:
            # Mock request for email context
            request = RequestFactory().get('/')

            # Context data for the welcome email
            context = {
                'email': self.email,
                'password': self.plain_password,  # Set a secure way to provide or generate this password
                'login_url': "http://142.93.210.192:8002/sign-in"  # Update with your login URL
            }

            # Send the welcome email
            send_welcome_user(request,self.email,context)

class CaseInsensitiveFieldMixin:
    """
    Field mixin that uses case-insensitive lookup alternatives if they exist.
    """
    LOOKUP_CONVERSIONS = {
        'exact': 'iexact',
        'contains': 'icontains',
        'startswith': 'istartswith',
        'endswith': 'iendswith',
        'regex': 'iregex',
    }
    def get_lookup(self, lookup_name):
        converted = self.LOOKUP_CONVERSIONS.get(lookup_name, lookup_name)
        return super().get_lookup(converted)


class CICharField(CaseInsensitiveFieldMixin, models.CharField):
    pass


class CIEmailField(CaseInsensitiveFieldMixin, models.EmailField):
    pass


class User(AbstractUser):

    type = models.CharField(choices=USER_TYPE_CHOICES, max_length=20, null=True)
    email = models.EmailField(blank=False, unique=True)
    plain_email_check = models.BooleanField(default=True, blank=True, null=True)
    plain_password = models.CharField(max_length=128, null=True)
    mobile_no = models.CharField(max_length=128, null=True,blank=True)
    is_deleted = models.BooleanField(null=False, default=False)
    city = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile = models.ImageField(blank=True, null=True)
    objects = SoftDeleteUserManager()
    objects_with_deleted = SoftDeleteUserManager(deleted=True)

    class Meta:
        app_label = 'user'

    def restore(self):
        self.is_deleted = False
        self.save()

    def delete_hard(self):
        super(User, self).delete()

    def set_password(self, raw_password):
        super().set_password(raw_password)
        if self.email:
            self.plain_password = raw_password
            self.save()


    def save(self, *args, **kwargs):
        # Check if the user is new (i.e., doesn't have a primary key yet)
        is_new_user = self.pk is None

        super().save(*args, **kwargs)  # Call the original save method to ensure the user is saved first

        # Only send the email if this is a new user
        if is_new_user:
            # Mock request for email context
            request = RequestFactory().get('/')

            # Context data for the welcome email
            context = {
                'email': self.email,
                'password': self.plain_password,  # Set a secure way to provide or generate this password
                'login_url': "http://142.93.210.192:8002/sign-in"  # Update with your login URL
            }

            # Send the welcome email
            send_welcome_user(request,self.email,context)


class TransactionDetails(DateTimeModel):
    mihpayid = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255, null=True, blank=True)
    mode = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255)
    tip = models.FloatField(max_length=255,null=True, blank=True)
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


class Subscription(DateTimeModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, related_name='subscriptions')
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, related_name='compaign_subscription')
    start_date = models.DateTimeField(default=timezone.now)
    razorpay_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f"{self.user.username} - {self.plan.name} (Active: {self.is_active})"





class TransactionDetails(DateTimeModel):

    mihpayid = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255, null=True, blank=True)
    mode = models.CharField(max_length=255, null=True, blank=True)
    cow_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255)
    tip = models.FloatField(max_length=255,null=True, blank=True)
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

class Subscription(DateTimeModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, related_name='subscriptions')
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, related_name='compaign_subscription')
    start_date = models.DateTimeField(default=timezone.now)
    cow_name = models.CharField(max_length=255, blank=True, null=True)
    razorpay_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f"{self.user.username} - {self.plan.name} (Active: {self.is_active})"
