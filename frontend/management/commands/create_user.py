import razorpay
from django.core.management.base import BaseCommand
from apps.user.models import SubscriptionPlan
from django.contrib.auth import get_user_model, authenticate, login, logout

from frontend.views import create_user

User = get_user_model()
from django.conf import settings


class Command(BaseCommand):
    help = 'Fetch and save subscription plans from Razorpay'

    def handle(self, *args, **kwargs):
        client = razorpay.Client(auth=(settings.RAZOR_PAY_ID, settings.RAZOR_PAY_SECRET))
        try:
            phone = "9898989898"
            first_name = "Test ji"
            email = "livingsparkglobal@gmail.com"
            password = "admin"
            city = "Japan"
            create_user(first_name,email,password,phone,'Devotee', city)

            self.stdout.write(self.style.SUCCESS('Successfully fetched and saved plans'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error fetching plans: {e}'))
