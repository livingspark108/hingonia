from django.contrib.auth import get_user_model
from django.db import models
from application.custom_model import DateTimeModel

User = get_user_model()
from django.db.models.signals import post_save
from django.dispatch import receiver
import random


class Promoter(DateTimeModel):
    mobile_no = models.CharField('Mobile no', max_length=128, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='promoter_user', null=True, blank=False)
    promoter_no = models.CharField('Promoter no', max_length=6, unique=True, editable=False)

@receiver(post_save, sender=Promoter)
def generate_promoter_no(sender, instance, created, **kwargs):
    if created:
        # Generate a unique 6-digit promoter number
        while True:
            random_number = str(random.randint(100000, 999999))
            if not Promoter.objects.filter(promoter_no=random_number).exists():
                instance.promoter_no = random_number
                break
        instance.save()
