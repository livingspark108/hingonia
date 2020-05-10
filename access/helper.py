from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


def check_permission(user, permission):
    if user.is_superuser:
        return True
    if user.role:
        role = user.role
        if role.name == 'Admin':
            return True
        permissions = role.permissions
        if permission in permissions:
            return True
    else:
        return False


class UserHasPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return check_permission(self.request.user, self.permission)

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorised to perform this action')
        referer = self.request.META.get('HTTP_REFERER', None)
        return redirect(referer if referer else 'dashboard')
