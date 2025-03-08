from django.contrib import admin

# Register your models here.
from apps.user.models import User,SubscriptionPlan,Subscription

admin.site.register(User)
admin.site.register(SubscriptionPlan)
admin.site.register(Subscription)