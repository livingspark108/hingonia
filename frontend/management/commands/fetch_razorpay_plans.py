import razorpay
from django.core.management.base import BaseCommand
from apps.user.models import SubscriptionPlan

from django.conf import settings


class Command(BaseCommand):
    help = 'Fetch and save subscription plans from Razorpay'

    def handle(self, *args, **kwargs):
        client = razorpay.Client(auth=(settings.RAZOR_PAY_ID, settings.RAZOR_PAY_SECRET))
        try:
            plans = client.plan.all()
            for plan in plans['items']:
                SubscriptionPlan.objects.update_or_create(
                    razorpay_plan_id=plan['id'],
                    defaults={
                        'name': plan['item']['name'],
                        'amount': plan['item']['amount'] / 100,  # Amount is in paise
                        'interval': plan['period'],
                    }
                )
            self.stdout.write(self.style.SUCCESS('Successfully fetched and saved plans'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error fetching plans: {e}'))
