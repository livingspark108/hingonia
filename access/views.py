from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, TemplateView

from project.custom_classes import ArthonsysDatatableView
from .models import Role

# Create your views here.


class CreateRoleView(LoginRequiredMixin, CreateView, SuccessMessageMixin):
    template_name = 'role_form.html'
    model = Role
    fields = ['name', 'slug', 'permissions']
    success_message = 'Role created successfully'
    success_url = reverse_lazy('list_role')


class UpdateRoleView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    template_name = 'role_form.html'
    model = Role
    fields = ['name', 'slug', 'permissions']
    success_message = 'Role updated successfully'
    success_url = reverse_lazy('list_role')

    def get_context_data(self, **kwargs):
        context = super(UpdateRoleView, self).get_context_data(**kwargs)
        context['checked_permissions'] = self.object.permissions
        return context


class ListRoleView(LoginRequiredMixin, TemplateView):
    template_name = 'role_list.html'


class ListRoleViewJson(ArthonsysDatatableView):
    model = Role
    columns = ['name', 'id']

    def render_column(self, row, column):

        if column == 'id':
            edit_action = '<a href={}><i class="fa fa-edit"></i></a>'.format(
                reverse('edit_role', kwargs={'pk': row.id}))
            if row.name != 'Admin' and row.name != 'admin':
                return edit_action
            else:
                return ""
        else:
            return super(ListRoleViewJson, self).render_column(row, column)
