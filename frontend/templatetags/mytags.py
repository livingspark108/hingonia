import re

from django import template
from django.urls import reverse, NoReverseMatch
import json
import pytz
from datetime import date
from django.utils import timezone
import dateutil.parser

utc=pytz.UTC
from datetime import datetime

register = template.Library()

@register.filter(name='convert_spaces_to_span')
def convert_spaces_to_span(value):
    return re.sub(r"'(.*?)'", r'<span>\1</span>', value)