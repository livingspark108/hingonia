

from django import template

from access.helper import check_permission

register = template.Library()


@register.simple_tag(takes_context=True)
def get_user_perm(context, permission):
    try:
        request = context['request']
        return check_permission(request.user, permission)
    except Exception as e:
        return False

