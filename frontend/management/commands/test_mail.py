# In your Django app, create a management/commands directory with an __init__.py file
# Then, create a fetch_plans.py file inside management/commands

from django.core.management.base import BaseCommand

from application.helper import fetch_and_save_plans_from_razorpay
from django.core.mail import send_mail

from application.settings.common import ADMIN_EMAIL


class Command(BaseCommand):
    help = 'Fetch and save subscription plans from Razorpay'

    def handle(self, *args, **kwargs):
        send_mail(
            'Subject here',
            'Here is the message.',
            ADMIN_EMAIL,  # From email
            ['rahulsoni270@gmail.com'],  # To email
            fail_silently=False,
        )
        self.stdout.write(self.style.SUCCESS('Successfully fetched and saved plans from Razorpay'))
