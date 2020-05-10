
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.views.decorators.cache import never_cache
import json

from settings.models import StateList


@method_decorator(never_cache, name='dispatch')
class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dashboard'))
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            login(request, user)
            if user.is_staff:
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                return HttpResponseRedirect(reverse('dashboard'))
        else:
            messages.error(request, 'Please check credentials.')
            return HttpResponseRedirect(reverse('sys_login'))


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, 'You have successfully logged out.')
        return render(request, 'login.html')


class ChangePasswordView(LoginRequiredMixin, View):
    """
    Change Password
    """
    def get(self, request):
        """
          dashboard
        """
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form': form})

    def post(self, request):
        """
          change password
        """

        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password has been successfully updated!')
        else:
            messages.error(request, 'Error occured while changing password, please enter a proper password.')
            return render(request, 'change_password.html', {'form': form})
        return redirect('change_password')


# class EmailValidationOnForgotPassword(PasswordResetForm):
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if not User.objects.filter(email__iexact=email, is_active=True).exists():
#             raise ValidationError("There is no user registered with the specified email address!")
#
#         return email

def load_state(request):
    f = open('statelist.json', )

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    for i in data:
       sl = StateList()
       sl.name = i['name']
       sl.country_code =  i['country']
       sl.save()
    # Closing file
    f.close()