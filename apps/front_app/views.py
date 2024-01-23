from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView

from apps.cms.models import Page
from application.custom_classes import AdminRequiredMixin, AjayDatatableView
from apps.front_app.models import Campaign, Mother, OurTeam, AboutUs


class CreateCampaignView(AdminRequiredMixin, SuccessMessageMixin, CreateView):

    model = Campaign
    fields = ['title','short_description', 'description','campaign_image']
    template_name = 'campaign/form.html'
    success_message = "%(title)s has been created successfully"
    success_url = reverse_lazy('campaign-list')


class ListCampaignView(AdminRequiredMixin, TemplateView):
    model = Campaign
    template_name = 'campaign/list.html'


class ListCampaignViewJson(AjayDatatableView):
    model = Campaign
    columns = ['title', 'actions']
    exclude_from_search_cloumn = ['actions']

    def render_column(self, row, column):
        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-sm mr-1">Edit</a>'.format(
                reverse('campaign-edit', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-sm" data-url={} role="button">Delete</a>'.format(
                reverse('campaign-delete', kwargs={'pk': row.pk}))
            return edit_action + delete_action
        else:
            return super(ListCampaignViewJson, self).render_column(row, column)


class UpdateCampaignView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Campaign
    fields = ['title','short_description', 'description','campaign_image']
    template_name = 'campaign/form.html'
    success_message = "%(title)s has been updated successfully"
    success_url = reverse_lazy('campaign-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateCampaignView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class DeleteCampaignView(AdminRequiredMixin, DeleteView):
    model = Campaign

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)

# Mother Modules

class CreateMotherView(AdminRequiredMixin, SuccessMessageMixin, CreateView):

    model = Mother
    fields = ['title', 'description','mother_image']
    template_name = 'mother/form.html'
    success_message = "%(title)s has been created successfully"
    success_url = reverse_lazy('mother-list')


class ListMotherView(AdminRequiredMixin, TemplateView):
    model = Mother
    template_name = 'mother/list.html'


class ListMotherViewJson(AjayDatatableView):
    model = Mother
    columns = ['title', 'actions']
    exclude_from_search_cloumn = ['actions']

    def render_column(self, row, column):
        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-sm mr-1">Edit</a>'.format(
                reverse('mother-edit', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-sm" data-url={} role="button">Delete</a>'.format(
                reverse('mother-delete', kwargs={'pk': row.pk}))
            return edit_action + delete_action
        else:
            return super(ListMotherViewJson, self).render_column(row, column)


class UpdateMotherView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Mother
    fields = ['title', 'description', 'mother_image']
    template_name = 'mother/form.html'
    success_message = "%(title)s has been updated successfully"
    success_url = reverse_lazy('mother-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateMotherView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class DeleteMotherView(AdminRequiredMixin, DeleteView):
    model = Mother

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)


# OurTeam Modules

class CreateOurTeamView(AdminRequiredMixin, SuccessMessageMixin, CreateView):

    model = OurTeam
    fields = ['title', 'designation','short_description','profile']
    template_name = 'ourteam/form.html'
    success_message = "%(title)s has been created successfully"
    success_url = reverse_lazy('ourteam-list')


class ListOurTeamView(AdminRequiredMixin, TemplateView):
    model = OurTeam
    template_name = 'ourteam/list.html'


class ListOurTeamViewJson(AjayDatatableView):
    model = OurTeam
    columns = ['title', 'actions']
    exclude_from_search_cloumn = ['actions']

    def render_column(self, row, column):
        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-sm mr-1">Edit</a>'.format(
                reverse('ourteam-edit', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-sm" data-url={} role="button">Delete</a>'.format(
                reverse('ourteam-delete', kwargs={'pk': row.pk}))
            return edit_action + delete_action
        else:
            return super(ListOurTeamViewJson, self).render_column(row, column)


class UpdateOurTeamView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):

    model = OurTeam
    fields = ['title', 'designation','short_description','profile']
    template_name = 'ourteam/form.html'
    success_message = "%(title)s has been updated successfully"
    success_url = reverse_lazy('ourteam-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateOurTeamView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class DeleteOurTeamView(AdminRequiredMixin, DeleteView):
    model = OurTeam

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)


# Update About us view

class UpdateAboutUsView(CreateView, UpdateView):
    model = AboutUs
    fields = ['title', 'description','banner']
    template_name = 'about-us/form.html'  # Provide the path to your template
    success_url = reverse_lazy('update-about-us')  # Specify the URL to redirect after successful creation or update

    def get_object(self, queryset=None):
        # If an object already exists, it's an update; otherwise, it's a create
        return AboutUs.objects.first()

