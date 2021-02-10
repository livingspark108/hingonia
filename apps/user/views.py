from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView
from application.custom_classes import AjayDatatableView
from apps.user.forms import CreateUserForm, EditUserForm

User = get_user_model()


class CreateUserView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'user/form.html'
    success_message = "User created successfully"
    success_url = reverse_lazy('user-list')


class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'user/form.html'
    success_message = "User updated successfully"
    success_url = reverse_lazy('user-list')


class ListUserView(LoginRequiredMixin, TemplateView):
    template_name = 'user/list.html'


class ListUserViewJson(AjayDatatableView):
    model = User
    columns = ['first_name', 'last_name', 'username', 'email', 'is_active', 'actions']
    exclude_from_search_cloumn = ['actions']
    # extra_search_columns = ['']

    def get_initial_queryset(self):
        return self.model.objects.filter(is_superuser=False).filter(type='admin')

    def render_column(self, row, column):
        if column == 'is_active':
            if row.is_active:
                return '<span class="badge badge-success">Active</span>'
            else:
                return '<span class="badge badge-danger">Inactive</span>'

        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-sm mr-1">Edit</a>'.format(
                reverse('user-edit', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-sm" data-url={} role="button">Delete</a>'.format(
                reverse('user-delete', kwargs={'pk': row.pk}))
            return edit_action + delete_action
        else:
            return super(ListUserViewJson, self).render_column(row, column)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)

