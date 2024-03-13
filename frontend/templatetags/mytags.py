import re

from django import template
from django.urls import reverse, NoReverseMatch
import json
import pytz
from datetime import date
from django.utils import timezone
import dateutil.parser

from apps.front_app.models import Campaign, Setting

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
