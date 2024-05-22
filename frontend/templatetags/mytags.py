import re
from django.db.models import Q

from django import template
from django.urls import reverse, NoReverseMatch
import json
import pytz
from datetime import date
from django.utils import timezone
import dateutil.parser
from django.db.models import Sum

from apps.front_app.models import Campaign, Setting
from apps.promoter.models import Promoter
from apps.user.models import TransactionDetails

utc=pytz.UTC
from datetime import datetime

register = template.Library()

@register.filter(name='convert_spaces_to_span')
def convert_spaces_to_span(value):
    return re.sub(r"'(.*?)'", r'<span>\1</span>', value)



@register.simple_tag()
def get_campain_data():
    return Campaign.objects.all()

@register.simple_tag()
def get_setting_data():
    return Setting.objects.first()

@register.filter(name='handle_none')
def handle_none(num):
    if not num:
        return ""
    else:
        return num

@register.filter(name='add_spam_tag')
def add_spam_tag(value):
    words = value.split()
    last_word = words[-1]
    modified_string = ' '.join(words[:-1]) + f' <span class="color-2">{last_word}</span>'
    return modified_string


@register.simple_tag()
def get_promo_detail(campaign_id,promo_no,start_date,end_date):
    # promo_obj = Promoter.
    print(campaign_id)
    print("Promo")
    print(promo_no)
    print("End")
    if start_date:
        cam_ob = TransactionDetails.objects.filter(Q(status='success') | Q(status='captured')).filter(
            campaign_id=campaign_id, promoter_no=promo_no).filter(Q(created_at__date__gte=start_date) & Q(created_at__date__lte=end_date))
    else:
        cam_ob = TransactionDetails.objects.filter(Q(status='success') | Q(status='captured')).filter(campaign_id=campaign_id,promoter_no=promo_no)
    tr_amt = cam_ob.aggregate(amount=Sum('amount'))['amount'] or 0

    context = {
                'count': cam_ob.count(),
                'amt': tr_amt,
                }
    return context