# In your Django app, create a management/commands directory with an __init__.py file
# Then, create a fetch_plans.py file inside management/commands

from django.core.management.base import BaseCommand

from application.helper import fetch_and_save_plans_from_razorpay


class Command(BaseCommand):
    help = 'Fetch and save subscription plans from Razorpay'

    def handle(self, *args, **kwargs):
        fetch_and_save_plans_from_razorpay()
        self.stdout.write(self.style.SUCCESS('Successfully fetched and saved plans from Razorpay'))
