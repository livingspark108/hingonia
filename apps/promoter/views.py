import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
import json
import time
from django.db import IntegrityError
from django.template.defaultfilters import lower
from datetime import datetime, timedelta, timezone
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView
from application.custom_classes import AjayDatatableView, ParentRequiredMixin, AdminRequiredMixin
from .forms import *
from .models import Promoter
from ..front_app.models import Campaign

User = get_user_model()

from django.utils.crypto import get_random_string


class CreatePromoterView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Promoter
    form_class = CreatePromoterForm
    user_form_class = CreatePromoterUserForm
    template_name = 'promoter/form.html'
    success_message = "Promoter created successfully"
    success_url = reverse_lazy('promoter-list')


    def get(self, request):
        form = self.form_class()
        user_form = self.user_form_class()

        return render(request, self.template_name, {'form': form, 'user_form': user_form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user_form = self.user_form_class(request.POST)

        if all([form.is_valid(), user_form.is_valid()]):
            user = user_form.save()
            promoter = form.save(commit=False)
            promoter.user = user
            promoter.save()
            messages.success(request, self.success_message)
        else:
            return render(request, self.template_name, {'form': form, 'user_form': user_form})
        return HttpResponseRedirect(self.success_url)




class UpdatePromoterView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Promoter
    form_class = EditPromoterForm
    user_form_class = EditPromoterUserForm
    template_name = 'promoter/form.html'
    success_message = "Promoter updated successfully"
    success_url = reverse_lazy('promoter-list')

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(UpdatePromoterView, self).get_context_data(**kwargs)
        if 'form_class' not in context:
            form = self.form_class(instance=self.object)
            context['form'] = form
        if 'user_form_class' not in context:
            context['user_form'] = self.user_form_class(instance=self.object.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        user_form = self.user_form_class(request.POST, instance=self.object.user)
        if all([form.is_valid(), user_form.is_valid()]):
            promoter = form.save()
            promoter.restaurant = request.user.restaurant_user
            promoter.save()
            user_form.save()
            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(
                self.get_context_data(parent_form=form, user_form=user_form))


class ListPromoterView(LoginRequiredMixin, TemplateView):
    template_name = 'promoter/list.html'


class ListPromoterViewJson(AjayDatatableView):
    model = Promoter
    columns = ['user.first_name', 'user.email', 'actions']
    exclude_from_search_cloumn = ['actions']

    # extra_search_columns = ['']

    def render_column(self, row, column):

        if column == 'user.is_active':
            if row.user:
                if row.user.is_active:
                    return '<span class="badge badge-success">Active</span>'
                else:
                    return '<span class="badge badge-danger">Inactive</span>'
            else:
                return ''


        if column == 'actions':
            link_action = '<a href={} role="button" class="btn btn-primary btn-sm mr-1">View Campaign</a>'.format(
                reverse('view-campaign', kwargs={'id': row.pk}))

            edit_action = '<a href={} role="button" class="btn btn-warning btn-sm mr-1">Edit</a>'.format(
                reverse('promoter-edit', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-sm" data-url={} role="button">Delete</a>'.format(
                reverse('promoter-delete', kwargs={'pk': row.pk}))

            return link_action + edit_action + delete_action
        else:
            return super(ListPromoterViewJson, self).render_column(row, column)


class DeletePromoterView(LoginRequiredMixin, DeleteView):
    model = Promoter

    def delete(self, request, *args, **kwargs):
        promoter = self.get_object()
        if promoter.user:
            promoter.user.delete()
        promoter.delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)

class ListCompaignPromoView(LoginRequiredMixin,View):
    def get(self,request,id):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        print(start_date)
        print(end_date)
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%d-%m-%Y').date()
            end_date = datetime.strptime(end_date, '%d-%m-%Y').date()
        else:
            start_date = ""
            end_date = ""
        #     campaign_obj = Campaign.objects.filter(Q(created_at__date__gte=start_date) & Q(created_at__date__lte=end_date))
        # else:
        campaign_obj = Campaign.objects.all()
        promoter_obj = Promoter.objects.get(id=id)
        context = {
            'start_date':start_date,
            'end_date': end_date,
            'campaign_obj':campaign_obj,
            'promoter_obj':promoter_obj
        }
        return render(request, 'promoter/dashboard.html', context)

