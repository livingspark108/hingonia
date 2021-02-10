from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.views.decorators.cache import never_cache
# importing plan
from django.contrib.auth import get_user_model
from application.custom_classes import AdminRequiredMixin, AjayDatatableView

User = get_user_model()
from django.http import HttpResponseRedirect


class AdminDashboardView(AdminRequiredMixin, View):

    def get(self, request):
        UserCount = User.objects.all().count()
        context = {
                    'UserCount': UserCount
                   }
        return render(request, 'administrator/dashboard.html', context)

