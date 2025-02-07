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
        email = 'livingsparkglobal@gmail.com'
        username = 'livingsparkglobal'
        phone = '9876543210'
        password = 'password'
        plain_password = 'password'

        additional_data = {
            'first_name': 'Test',
            'last_name': '',
            'mobile_no': phone,  # Ensure this field exists in your User model
            'city': '',  # Ensure this field exists in your User model
        }
        filtered_data = {k: v for k, v in additional_data.items() if k != "mobile_no"}

        user_obj = User.objects.create(
            email=email,
            username=username,
            mobile_no=phone,
            plain_password=password,
            type=type,  # Ensure `type` exists in your User model
            **filtered_data  # Additional data without 'mobile_no'
        )


        # ✅ Set and hash password
        user_obj.set_password(password)
        user_obj.save()
        self.stdout.write(self.style.SUCCESS('Successfully fetched and saved plans from Razorpay'))
