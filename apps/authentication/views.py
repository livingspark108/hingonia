from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.views.decorators.cache import never_cache
# importing plan
from django.contrib.auth import get_user_model
from application.custom_classes import AdminRequiredMixin

User = get_user_model()
from django.http import HttpResponseRedirect


@method_decorator(never_cache, name='dispatch')
class LoginView(View):
    template_name = 'auth/login.html'
    success_url = 'admin-dashboard'
    school_success_url = 'school-dashboard'
    teacher_success_url = 'teacher-dashboard'
    guide_success_url = 'guide-dashboard'
    parent_success_url = 'parent-dashboard'
    student_success_url = 'home'
    supervisor_success_url = 'supervisor-dashboard'
    login_url = 'auth-login'
    success_message = 'You have successfully logged in.'
    failure_message = 'Sorry, unrecognized username or password. Have you forgotten your password?.'

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.type == 'admin':
                return HttpResponseRedirect(reverse(self.success_url))
            elif user.type == 'school':
                return HttpResponseRedirect(reverse(self.school_success_url))
            elif user.type == 'teacher':
                return HttpResponseRedirect(reverse(self.teacher_success_url))
            elif user.type == 'student':
                return HttpResponseRedirect(reverse(self.student_success_url))
            elif user.type == 'parent':
                return HttpResponseRedirect(reverse(self.parent_success_url))
            elif user.type == 'guide':
                return HttpResponseRedirect(reverse(self.guide_success_url))
            elif user.type == 'supervisor':
                return HttpResponseRedirect(reverse(self.supervisor_success_url))
        return render(request, self.template_name)

    def post(self, request):
        user_input = request.POST['username']
        try:
            username = User.objects.get(email=user_input).username
        except User.DoesNotExist:
            username = user_input
        user = authenticate(request, username=username,
                            password=request.POST['password'])
        if user:
            login(request, user)
            messages.success(request, self.success_message)
            if user.is_staff or user.type == 'admin':
                return HttpResponseRedirect(reverse(self.success_url))
            elif user.type == 'school':
                return HttpResponseRedirect(reverse(self.school_success_url))
            elif user.type == 'teacher':
                return HttpResponseRedirect(reverse(self.teacher_success_url))
            elif user.type == 'student':
                return HttpResponseRedirect(reverse(self.student_success_url))
            elif user.type == 'parent':
                return HttpResponseRedirect(reverse(self.parent_success_url))
            elif user.type == 'guide':
                return HttpResponseRedirect(reverse(self.guide_success_url))
            elif user.type == 'supervisor':
                return HttpResponseRedirect(reverse(self.supervisor_success_url))
        else:
            messages.error(request, self.failure_message)
            return HttpResponseRedirect(reverse(self.login_url))


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, 'You have successfully logged out.')
        #return render(request, 'auth/login.html')
        return redirect('home')


class ChangeSelfPasswordView(AdminRequiredMixin, View):
    template_name = 'auth/change_password.html'

    def get(self, request,user_id):
        form = PasswordChangeForm(User.objects.get(pk=user_id))
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password has been successfully updated!')
        else:
            messages.error(request, 'Error occured while changing password, please enter a proper password.')
            return render(request, self.template_name, {'form': form})
        return redirect('admin-dashboard')


class ChangePasswordView(AdminRequiredMixin, View):
    template_name = 'auth/change_password.html'

    def get(self, request, user_id):
        form = PasswordChangeForm(User.objects.get(pk=user_id))
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password has been successfully updated!')
        else:
            messages.error(request, 'Error occured while changing password, please enter a proper password.')
            return render(request, self.template_name, {'form': form})
        return redirect('admin-dashboard')

