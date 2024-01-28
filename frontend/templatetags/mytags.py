import re

from django import template
from django.urls import reverse, NoReverseMatch
import json
import pytz
from datetime import date
from django.utils import timezone
import dateutil.parser

from apps.front_app.models import Campaign

utc=pytz.UTC
from datetime import datetime

register = template.Library()

@register.filter(name='convert_spaces_to_span')
def convert_spaces_to_span(value):
    return re.sub(r"'(.*?)'", r'<span>\1</span>', value)


@register.simple_tag()
def get_campain_data():
    return Campaign.objects.all()

@register.filter(name='handle_none')
def handle_none(num):
    if not num:
        return ""
    else:
        return num