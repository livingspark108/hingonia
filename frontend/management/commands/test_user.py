# In your Django app, create a management/commands directory with an __init__.py file
# Then, create a fetch_plans.py file inside management/commands

from django.core.management.base import BaseCommand

from application.helper import fetch_and_save_plans_from_razorpay
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from application.settings.common import ADMIN_EMAIL
User = get_user_model()

class Command(BaseCommand):
    help = 'Fetch and save subscription plans from Razorpay'

    def handle(self, *args, **kwargs):
        user_obj = User.objects.get(username='6b9a5b72-2b4d-4b7e-aa66-1296dcc18c75')
        user_obj.save_image_from_url('/media/uploads/campaign-bg_9RbF0TC.webp')
        self.stdout.write(self.style.SUCCESS('Successfully fetched and saved plans from Razorpay'))
