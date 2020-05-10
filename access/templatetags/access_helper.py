
from django import template

from access.constants import PERMISSION_TEXT

register = template.Library()


@register.filter
def get_description(value):
    print(value)
    description = PERMISSION_TEXT.get(value)
    if description:
        return description
    else:
        return ''

