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

