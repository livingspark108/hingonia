import json

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
from apps.user.models import TransactionDetails

User = get_user_model()
from django.db.models import Q


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        json_file_path = './cities_list.json'
        with open(json_file_path, 'r') as json_file:
            cities = json.load(json_file)

        # Add the transaction_id to the context
        context['cities'] = cities
        return context


class ListUserViewJson(AjayDatatableView):
    model = User
    columns = ['first_name', 'last_name', 'username', 'email','city', 'is_active', 'actions']
    exclude_from_search_cloumn = ['actions']
    # extra_search_columns = ['']

    def get_initial_queryset(self):
        print(self.request.GET.get('city', None))
        if self.request.GET.get('city', None):
            city = self.request.GET.get('city', None)
            return User.objects.filter(city__icontains=city).filter(is_superuser=False).filter(type='devotee').order_by('-id')
        else:
            return User.objects.filter(is_superuser=False).filter(Q(type='devotee') | Q(type='Devotee')).order_by('-id')


    def render_column(self, row, column):
        if column == 'is_active':
            if row.is_active:
                return '<span class="badge badge-success">Active</span>'
            else:
                return '<span class="badge badge-danger">Inactive</span>'
        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-sm mr-1">Edit</a>'.format(
                reverse('user-edit', kwargs={'pk': row.pk}))
            view_detail = '<a href={} role="button" class="btn btn-primary btn-sm mr-1">View Transaction</a>'.format(
                reverse('transaction-detail-list', kwargs={'pk': row.pk}))
            return edit_action + view_detail
        else:
            return super(ListUserViewJson, self).render_column(row, column)


class ListTransactionDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'user/transaction_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the ID from the URL parameters or request data
        transaction_id = self.kwargs.get('pk')  # Assuming 'id' is passed as a URL parameter

        # Add the transaction_id to the context
        context['transaction_id'] = transaction_id

        return context

class ListTransactionDetailViewJson(AjayDatatableView):
    model = TransactionDetails
    columns = ['mihpayid', 'mode', 'status', 'amount', 'created_at']
    exclude_from_search_cloumn = ['actions']
    # extra_search_columns = ['']

    def get_initial_queryset(self):
        id = self.kwargs['pk']
        user_obj = User.objects.get(id=id)
        return self.model.objects.filter(phone=user_obj.username)

    def render_column(self, row, column):
        if column == 'is_active':
            if row.is_active:
                return '<span class="badge badge-success">Active</span>'
            else:
                return '<span class="badge badge-danger">Inactive</span>'

        if column == 'actions':
            return ""
        else:
            return super(ListTransactionDetailViewJson, self).render_column(row, column)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)





