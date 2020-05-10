from django.shortcuts import render, get_object_or_404, redirect

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import exception_handler

from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.template import loader

from django.contrib.auth import get_user_model
from rest_framework import status


User = get_user_model()


################################  Dashboard #################################

class UserOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.id == self.kwargs['pk']

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorised to perform this action')
        return redirect('sys_login')


class DashboardView(LoginRequiredMixin, View):
    """
    Dashboard
    """

    def get(self, request):
        """
          dashboard
        """

        user_count = User.objects.filter(is_staff=False, is_active=True).count()

        return render(request, 'dashboard.html', {'user_count': user_count})


class ListUsersView(LoginRequiredMixin, ListView):
    """
    List Users
    """
    model = User
    queryset = User.objects.all()
    template_name = 'user/user_list.html'

    def get_queryset(self):
        """
        Return the list of items for this view.
        """
        queryset = User.objects.filter(is_staff=False)
        return queryset


class DetailUserView(LoginRequiredMixin, DetailView):
    """
    Detail of user
    """
    model = User
    template_name = 'user/user_detail.html'


class CreateUserView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new user
    """
    model = User
    fields = ['first_name', 'last_name', 'username', 'email', 'phone_no', 'address_1', 'address_2', 'city', 'country',
              'state', 'zip_code', 'image', 'password', 'role', 'is_active']
    template_name = 'user/user_form.html'
    success_message = "%(username)s has been created successfully"
    success_url = reverse_lazy('list_users')

    def get_context_data(self, **kwargs):
        context = super(CreateUserView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        print(form.data)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save()
            user.set_password(request.POST['password'])
            user.save()
        else:
            return render(request, self.template_name, {'form': form})
        messages.success(request, "{}, user added successfully.".format(user.username))
        return HttpResponseRedirect(reverse('list_users'))


class UpdateUserView(LoginRequiredMixin, UserOrAdminMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing user
    """

    model = User

    template_name = 'user/user_form.html'
    success_message = "%(username)s has been updated successfully"

    def get_context_data(self, **kwargs):
        context = super(UpdateUserView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            self.fields = ['first_name', 'last_name', 'username', 'email', 'address_1', 'address_2', 'city', 'country',
                           'state', 'zip_code', 'image', 'role', 'is_active']
            if request.user.id == kwargs['pk']:
                self.fields = ['first_name', 'last_name', 'username', 'email']
                self.success_url = reverse_lazy('dashboard')
            else:
                self.success_url = reverse_lazy('user_detail', kwargs={'pk': kwargs['pk']})
        else:
            self.success_message = "Your account has been updated successfully"
            self.fields = ['first_name', 'last_name', 'username', 'email', 'address_1', 'address_2', 'city', 'country',
                           'state', 'zip_code', 'image', 'role', 'is_active']
            self.success_url = reverse_lazy('user_detail', kwargs={'pk': self.request.user.id})
        return super().dispatch(request, *args, **kwargs)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    """
    Delete existing user
    """
    model = User
    template_name = 'user/user_confirm_delete.html'
    success_message = "User has been deleted successfully"
    success_url = reverse_lazy('list_users')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteUserView, self).delete(request, *args, **kwargs)


def redirect_dashboard(request):
    response = redirect('dashboard')
    return response


def change_user_status(request, pk, status):
    user = User.objects.get(pk=pk)
    user.is_active = status
    user.save()
    return redirect(request.META['HTTP_REFERER'])



