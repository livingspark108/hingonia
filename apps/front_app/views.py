from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView

from apps.cms.models import Page
from application.custom_classes import AdminRequiredMixin, AjayDatatableView
from apps.front_app.forms import CreateDistributionForm, DistributionImageFormset
from apps.front_app.models import Campaign, Mother, OurTeam, AboutUs, Distribution
from django.contrib import messages

from apps.user.models import TransactionDetails


class CreateCampaignView(AdminRequiredMixin, SuccessMessageMixin, CreateView):

    model = Campaign
    fields = ['title','short_title','price','short_description', 'description','campaign_image']
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
    fields = ['title','short_title','price','short_description', 'description','campaign_image']
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

class ListDonationView(AdminRequiredMixin, TemplateView):
    model = TransactionDetails
    template_name = 'donation/list.html'

class ListDonationViewJson(AjayDatatableView):
    model = TransactionDetails
    columns = ['phone','amount','mode','status','created_at', 'actions']
    exclude_from_search_cloumn = ['actions']

    def render_column(self, row, column):
        if column == 'actions':

            return ''
        else:
            return super(ListDonationViewJson, self).render_column(row, column)

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


# Distribution ( Create )
class CreateDistributionView(AdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = Distribution
    form_class = CreateDistributionForm
    template_name = 'distribution/form.html'
    success_message = "%(title)s has been created successfully"
    success_url = reverse_lazy('distribution-list')
    object = None


    def get_form_kwargs(self):
        kwargs = super(CreateDistributionView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, *args, **kwargs):

        form = self.form_class()
        distribution_image_form = DistributionImageFormset()
        return self.render_to_response(
            self.get_context_data(
                form=form,
                distribution_image_form=distribution_image_form,
            )
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        distribution_image_form = DistributionImageFormset(request.POST, request.FILES)
        print(distribution_image_form)
        if form.is_valid() and distribution_image_form.is_valid():
            self.object = form.save()
            distribution_image_form.save(commit=False)
            distribution_image_form.instance = self.object
            distribution_image_form.save()
            self.object.save()
            messages.success(request, self.success_message)
        else:
            return render(request, self.template_name, {'form': form, 'distribution_item_form': distribution_image_form, })

        return HttpResponseRedirect(self.success_url)




class UpdateDistributionView(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Distribution
    form_class = CreateDistributionForm
    template_name = 'distribution/form.html'
    success_message = "Distribution updated successfully"
    success_url = reverse_lazy('distribution-list')

    def get(self, request, pk, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        distribution_image_form = DistributionImageFormset(instance=self.object)

        return self.render_to_response(
            self.get_context_data(form=form,
                                  distribution_image_form=distribution_image_form,
                                  )
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(self.request.POST, self.request.FILES, instance=self.object)
        distribution_image_form = DistributionImageFormset(self.request.POST,self.request.FILES, instance=self.object)

        if form.is_valid() and distribution_image_form.is_valid():
            return self.form_valid(form, distribution_image_form)
        else:
            return self.form_invalid(form, distribution_image_form)

    def form_valid(self, form, distribution_image_form):
        self.object = form.save()
        distribution_image_form.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, distribution_image_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  distribution_image_form=distribution_image_form,
                                  )
        )


class ListDistributionView(AdminRequiredMixin, TemplateView):
    model = Distribution
    template_name = 'distribution/list.html'


class ListDistributionViewJson(AjayDatatableView):
    model = Distribution
    columns = ['title', 'actions']
    exclude_from_search_cloumn = ['actions']

    def render_column(self, row, column):
        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-sm mr-1">Edit</a>'.format(
                reverse('distribution-edit', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-sm" data-url={} role="button">Delete</a>'.format(
                reverse('distribution-delete', kwargs={'pk': row.pk}))
            return edit_action + delete_action
        else:
            return super(ListDistributionViewJson, self).render_column(row, column)


class DeleteDistributionView(AdminRequiredMixin, DeleteView):
    model = Distribution
    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)