import logging

from django.utils import timezone
from django.db.models import Sum
from datetime import datetime,time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView

from application.email_helper import WhatsAppThread
from application.helper import WhatsAppSenderThread
from apps.cms.models import Page
from application.custom_classes import AdminRequiredMixin, AjayDatatableView
from apps.front_app.constants import SLIDER_TYPE, CAMPAIGN_TYPE, MODE_TYPE
from apps.front_app.forms import CreateDistributionForm, CreateCampaignForm, \
    CampaignImageFormset, HomePageCampaignForm, CreateTestimonialForm, CreateTrusteeForm, CreateOurSupporterForm
from apps.front_app.models import Campaign, Mother, OurTeam, AboutUs, Distribution, Setting, AbandonCart, Product, \
    CampaignProduct, UploadedFile, HomePageCampaign, Order, Testimonial, HomeSlider, Trustee, OurSupporter, \
    HomePageContent
from django.contrib import messages

from apps.user.forms import CreateSubscriberForm
from apps.user.models import TransactionDetails, SubscriptionPlan, Subscription

logger = logging.getLogger('custom_logger')

class CreateCampaignView(AdminRequiredMixin, SuccessMessageMixin, CreateView):

    model = Campaign
    form_class = CreateCampaignForm
    template_name = 'campaign/form.html'
    success_message = "%(title)s has been created successfully"
    success_url = reverse_lazy('campaign-list')
    object = None

    def get_form_kwargs(self):
        kwargs = super(CreateCampaignView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, *args, **kwargs):

        form = self.form_class()
        return self.render_to_response(
            self.get_context_data(
                form=form,
            )
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save()
            messages.success(request, self.success_message)
        else:
            return render(request, self.template_name,
                          {'form': form })

        return HttpResponseRedirect(self.success_url)


class ListCampaignView(AdminRequiredMixin, TemplateView):
    model = Campaign
    template_name = 'campaign/list.html'

    def get_context_data(self, **kwargs):
        context = super(ListCampaignView, self).get_context_data(**kwargs)
        context['campaign_type'] = CAMPAIGN_TYPE
        context['mode_type'] = MODE_TYPE
        return context


class ListCampaignViewJson(AjayDatatableView):
    model = Campaign
    columns = ['title','type','mode','is_home','price', 'actions']
    exclude_from_search_cloumn = ['actions']

    def get_initial_queryset(self):
        print(self.request.GET)

        campaign_type = self.request.GET.getlist('campaign_type[]')
        mode_type = self.request.GET.getlist('mode_type[]')

        filters_fileds = Q()
        if campaign_type:
            campaign_type = campaign_type[0]
            if campaign_type:
                filters_fileds.add(Q(type=campaign_type), Q.AND)

        if mode_type:
            mode_type = mode_type[0]
            if mode_type:
                filters_fileds.add(Q(mode=mode_type), Q.AND)


        return self.model.objects.filter(filters_fileds).order_by('-created_at')


    def render_column(self, row, column):
        if column == 'is_home':
            if row.is_home:
                return "<i class='mdi mdi-star mark_fav active_fav' data-id='{}' style='text-align: center;font-size: 30px;cursor: pointer;'></i>".format(row.pk)
            else:
                return "<i class='mdi mdi-star mark_fav' data-id='{}' style='text-align: center;font-size: 30px;cursor: pointer;'></i>".format(row.pk)

        if column == 'actions':
            if row.type == 'Temple':
                like_action = '<a href={} role="button" target="blank" class="btn btn-primary btn-sm mr-1">Link</a>'.format(
                    reverse('temple_single', kwargs={'slug': row.slug}))
            else:
                like_action = '<a href={} role="button" target="blank" class="btn btn-primary btn-sm mr-1">Link</a>'.format(
                    reverse('ongoing-devotion', kwargs={'id': row.slug}))

            clone_action = '<a href={} role="button" class="btn btn-info btn-sm mr-1">Clone</a>'.format(
                reverse('campaign-clone', kwargs={'pk': row.pk}))

            edit_action = '<a href={} role="button" class="btn btn-warning btn-sm mr-1">Edit</a>'.format(
                reverse('campaign-edit', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-sm" data-url={} role="button">Delete</a>'.format(
                reverse('campaign-delete', kwargs={'pk': row.pk}))
            return like_action + edit_action + clone_action +  delete_action
        else:
            return super(ListCampaignViewJson, self).render_column(row, column)


class UpdateCampaignView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Campaign
    form_class = CreateCampaignForm
    template_name = 'campaign/form.html'
    success_message = "Campaign updated successfully"
    success_url = reverse_lazy('campaign-list')

    def get(self, request, pk, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        campaign_image_form = CampaignImageFormset(instance=self.object)

        return self.render_to_response(
            self.get_context_data(form=form,
                                  campaign_image_form=campaign_image_form,
                                  )
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(self.request.POST, self.request.FILES, instance=self.object)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  )
        )

class DeleteCampaignView(AdminRequiredMixin, DeleteView):
    model = Campaign

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)

class CloneCampaignView(AdminRequiredMixin,View):
    def get(self,request,pk):
        print("HERE")
        print(pk)
        # Fetch the original object
        original_object = get_object_or_404(Campaign, pk=pk)

        # Clone the object by setting its primary key to None
        original_object.pk = None
        original_object.title = original_object.title+"-Copy"
        original_object.slug = original_object.slug+"-Copy"
        original_object.save()

        # Redirect to the detail page of the cloned object (or anywhere else)
        return redirect('campaign-edit', pk=original_object.pk)


# Campaign Product
class CreateCampaignProductView(AdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = CampaignProduct
    fields = ['title','unit_title','image','goal','price']
    template_name = 'campaign-product/form.html'
    success_message = "%(title)s has been created successfully"
    success_url = reverse_lazy('campaign-product-list')


class ListCampaignProductView(AdminRequiredMixin, TemplateView):
    model = CampaignProduct
    template_name = 'campaign-product/list.html'


class ListCampaignProductViewJson(AjayDatatableView):
    model = CampaignProduct
    columns = ['title','goal','price','actions']
    exclude_from_search_cloumn = ['actions']

    def render_column(self, row, column):
        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-sm mr-1">Edit</a>'.format(
                reverse('campaign-product-edit', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-sm" data-url={} role="button">Delete</a>'.format(
                reverse('campaign-product-delete', kwargs={'pk': row.pk}))
            clone_action = '<a href="javascript:;" class="confirm ml-1 btn btn-primary btn-sm" data-url={} role="button">Clone</a>'.format(
                reverse('campaign-product-clone', kwargs={'pk': row.pk}))

            return edit_action + delete_action + clone_action
        else:
            return super(ListCampaignProductViewJson, self).render_column(row, column)


class UpdateCampaignProductView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):

    model = CampaignProduct
    fields = ['title','unit_title','image','goal','price']
    template_name = 'campaign-product/form.html'
    success_message = "%(title)s has been updated successfully"
    success_url = reverse_lazy('campaign-product-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateCampaignProductView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class DeleteCampaignProductView(AdminRequiredMixin, DeleteView):
    model = CampaignProduct

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)


class CloneCampaignProductView(AdminRequiredMixin,View):
    def get(self,request,pk):
        print("HERE")
        print(pk)
        # Fetch the original object
        original_object = get_object_or_404(CampaignProduct, pk=pk)

        # Clone the object by setting its primary key to None
        original_object.pk = None
        original_object.title = original_object.title+"-Copy"
        original_object.save()

        # Redirect to the detail page of the cloned object (or anywhere else)
        return redirect('campaign-product-edit', pk=original_object.pk)


# Mother Modules

class CreateMotherView(AdminRequiredMixin, SuccessMessageMixin, CreateView):

    model = Mother
    fields = ['title','title_hindi', 'description', 'description_hindi','mother_image']
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch one object, for example, the first one
        context['campaign'] = Campaign.objects.all()
        total_amount = Campaign.objects.aggregate(Sum('price'))['price__sum'] or 0
        context['total_amount'] = total_amount
        return context

class ListDonationViewJson(AjayDatatableView):
    model = TransactionDetails
    columns = ['firstname','mihpayid','phone','amount','mode','status','productinfo','created_at', 'actions']
    exclude_from_search_cloumn = ['actions']

    def get_initial_queryset(self):
        start_date = self.request.GET.getlist('start_date[]')[0]
        end_date = self.request.GET.getlist('end_date[]')[0]
        campaign = self.request.GET.getlist('campaign[]')[0]
        print(start_date)
        print(end_date)

        # Calculate total amount based on campaign filter

        filters_fields = Q()

        # Handle start_date (start from 12:00 AM)
        if start_date:
            start_date = datetime.strptime(start_date, '%d-%m-%Y')  # Parse the date
            start_datetime = datetime.combine(start_date, time.min)  # Set to 12:00 AM
            filters_fields &= Q(created_at__gte=start_datetime)  # Greater than or equal to start_datetime

        # Handle end_date (end at 11:59 PM)
        if end_date:
            end_date = datetime.strptime(end_date, '%d-%m-%Y')  # Parse the date
            end_datetime = datetime.combine(end_date, time.max)  # Set to 11:59 PM
            filters_fields &= Q(created_at__lte=end_datetime)  # Less than or equal to end_datetime
        print(filters_fields)
        if campaign:
            # Apply campaign filter and calculate total amount
            self.total_amount = (
                    self.model.objects.filter(productinfo__icontains=campaign)
                    .filter(Q(status='captured') | Q(status='success'))
                    .filter(filters_fields)
                    .aggregate(Sum('amount'))['amount__sum'] or 0
            )
            self.total_tip = (
                    self.model.objects.filter(productinfo__icontains=campaign)
                    .filter(Q(status='captured') | Q(status='success'))
                    .filter(filters_fields)
                    .aggregate(Sum('tip'))['tip__sum'] or 0
            )
            # Return filtered queryset ordered by creation date
            return self.model.objects.filter(filters_fields) \
                .filter(productinfo__icontains=campaign) \
                .filter(Q(status='captured') | Q(status='success')) \
                .order_by('-created_at')
        else:
            print("Full data")
            # Calculate total amount without campaign filter
            self.total_amount = (
                    self.model.objects.filter(Q(status='captured') | Q(status='success')).filter(filters_fields).aggregate(Sum('amount'))['amount__sum'] or 0
            )
            self.total_tip = (
                    self.model.objects.filter(Q(status='captured') | Q(status='success')).filter(
                        filters_fields).aggregate(Sum('tip'))['tip__sum'] or 0
            )
            # Return filtered queryset ordered by creation date
            return self.model.objects.filter(Q(status='captured') | Q(status='success')).filter(filters_fields).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add total_amount to the context
        context['total_amount'] = self.total_amount
        context['total_tip'] = round(self.total_tip, 2)
        return context
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

#Update Setting

# Update About us view
class UpdateSettingView(CreateView,SuccessMessageMixin, UpdateView):
    model = Setting
    fields = '__all__'
    template_name = 'setting/form.html'  # Provide the path to your template
    success_url = reverse_lazy('setting')  # Specify the URL to redirect after successful creation or update
    success_message = "Setting has been updated successfully"

    def get_object(self, queryset=None):
        # If an object already exists, it's an update; otherwise, it's a create
        return Setting.objects.first()


class UpdateHomePageSettingView(CreateView,SuccessMessageMixin, UpdateView):
    model = HomePageContent
    fields = '__all__'
    template_name = 'setting/form.html'  # Provide the path to your template
    success_url = reverse_lazy('home-page-setting')  # Specify the URL to redirect after successful creation or update
    success_message = "Home Setting has been updated successfully"

    def get_object(self, queryset=None):
        # If an object already exists, it's an update; otherwise, it's a create
        return HomePageContent.objects.first()


class UpdateAboutUsView(CreateView,SuccessMessageMixin, UpdateView):
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
        return self.render_to_response(
            self.get_context_data(
                form=form,
            )
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save()

            messages.success(request, self.success_message)
        else:
            return render(request, self.template_name, {'form': form })

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

        return self.render_to_response(
            self.get_context_data(form=form,
                                  )
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(self.request.POST, self.request.FILES, instance=self.object)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form,
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


#Send whatsapp
class WhatsAppDashboardView(AdminRequiredMixin, View):
    def get(self, request):
        customer_number = TransactionDetails.objects.values_list('phone',flat=True).distinct()
        print(customer_number)
        customer_number = [string for string in customer_number if
                           string is not None and len(string) >= 10 and string.isdigit()]

        all_number = set(customer_number)
        context = {
            'all_number':all_number
        }
        return render(request, 'setting/whatsapp_dashboard.html', context)

    def post(self, request):
        all_contact = request.POST.getlist('contact_number')
        message = request.POST.get('message')
        setting_obj = Setting.objects.first()

        if setting_obj and setting_obj.whatsapp_key:
            key = setting_obj.whatsapp_key
            # Start the background thread to handle messaging
            WhatsAppSenderThread(all_contact, message, key).start()

        messages.success(request, "Message queue has started successfully.")

        return HttpResponseRedirect(reverse('whatsapp'))


# 80G request list
class List80GRequestView(AdminRequiredMixin, TemplateView):
    model = TransactionDetails
    template_name = '80gRequest/list.html'


# 80G request list ajax
class List80GRequestViewJson(AjayDatatableView):
    model = TransactionDetails
    columns = ['phone','amount','mode','status','created_at', 'actions']
    exclude_from_search_cloumn = ['actions']

    def get_initial_queryset(self):
        return TransactionDetails.objects.filter(is_80g_request=True,is_80g_request_approve=False).order_by(
            '-created_at')

    def render_column(self, row, column):
        if column == 'actions':
            approve_action = '<a href={} role="button" class="btn btn-success btn-sm mr-1">Approve</a>'.format(
                reverse('80g-request-approve', kwargs={'id': row.pk}))
            return approve_action
        else:
            return super(List80GRequestViewJson, self).render_column(row, column)


class Apporve80GView(View):
    def get(self, request,id):
        transaction_obj = TransactionDetails.objects.get(id=id)
        transaction_obj.is_80g_request_approve = True
        transaction_obj.save()
        return HttpResponseRedirect(reverse_lazy('80g-request-list'))


#
class ListAbandonView(AdminRequiredMixin, TemplateView):
    model = AbandonCart
    template_name = 'abandon/list.html'

class ListAbandonViewJson(AjayDatatableView):
    model = AbandonCart
    columns = ['full_name','email','mobile_no','created_at', 'actions']
    exclude_from_search_cloumn = ['actions']

    def get_initial_queryset(self):
        transaction_obj = TransactionDetails.objects.values_list('phone', flat=True)
        return AbandonCart.objects.exclude(mobile_no__in=transaction_obj)

    def render_column(self, row, column):
        if column == 'actions':

            return ''
        else:
            return super(ListAbandonViewJson, self).render_column(row, column)

class ListSubscriberView(AdminRequiredMixin, TemplateView):
    model = Subscription
    template_name = 'monthly_subscriber/list.html'

class ListSubscriberViewJson(AjayDatatableView):
    model = Subscription
    columns = ['email','subscription_id','plan','status', 'actions']
    exclude_from_search_cloumn = ['actions']


    def render_column(self, row, column):
        if column == 'actions':

            return ''
        else:
            return super(ListSubscriberViewJson, self).render_column(row, column)


class CreateProductView(AdminRequiredMixin, SuccessMessageMixin, CreateView):

    model = Product
    fields = ['title','price','short_description','description']
    template_name = 'product/form.html'
    success_message = "%(title)s has been created successfully"
    success_url = reverse_lazy('product-list')


class ListProductView(AdminRequiredMixin, TemplateView):
    model = Product
    template_name = 'product/list.html'


class ListProductViewJson(AjayDatatableView):
    model = Product
    columns = ['title','price', 'actions']
    exclude_from_search_cloumn = ['actions']

    def render_column(self, row, column):
        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-sm mr-1">Edit</a>'.format(
                reverse('product-edit', kwargs={'pk': row.pk}))
            clone_action = '<a href={} role="button" class="btn btn-info btn-sm mr-1">Clone</a>'.format(
                reverse('product-clone', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-sm" data-url={} role="button">Delete</a>'.format(
                reverse('product-delete', kwargs={'pk': row.pk}))
            return edit_action + clone_action + delete_action
        else:
            return super(ListProductViewJson, self).render_column(row, column)


class UpdateProductView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Product
    fields = ['title','price','short_description','description']
    template_name = 'product/form.html'
    success_message = "%(title)s has been updated successfully"
    success_url = reverse_lazy('product-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateProductView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class DeleteProductView(AdminRequiredMixin, DeleteView):
    model = Product

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)


class CloneProductView(AdminRequiredMixin,View):
    def get(self,request,pk):
        print("HERE")
        print(pk)
        # Fetch the original object
        original_object = get_object_or_404(Product, pk=pk)

        # Clone the object by setting its primary key to None
        original_object.pk = None
        original_object.title = original_object.title+"-Copy"
        original_object.save()

        # Redirect to the detail page of the cloned object (or anywhere else)
        return redirect('product-edit', pk=original_object.pk)



def file_upload_view(request):
    if request.method == 'POST':
        file = request.FILES['file']
        uploader_id = request.POST['uploader_id']
        file_type = request.POST['file_type']
        uploaded_file = UploadedFile(file=file,uploader_id=uploader_id,file_type=file_type)
        uploaded_file.save()
        return JsonResponse({'message': 'File uploaded successfully'})
    return render(request, 'campaign/upload.html')

def file_list_view(request):
    id = request.GET.get('id')
    type = request.GET.get('type')
    print(id)
    print(type)
    files = UploadedFile.objects.filter(uploader_id=id,file_type=type)
    print(files)
    return render(request, 'campaign/file_list.html', {'files': files})

@require_POST
def file_delete_view(request):
    file_id = request.POST.get('id')
    file = get_object_or_404(UploadedFile, id=file_id)
    file.file.delete()
    file.delete()
    return JsonResponse({'message': 'File deleted successfully'})

class HomePageSettingView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = HomePageCampaign
    form_class = HomePageCampaignForm
    template_name = 'home_page_setting/form.html'
    success_message = 'Home Page setting updated successfully'
    success_url = reverse_lazy('home-page-setting')

    def get_object(self, queryset=None):
        product_kitchen, _ = self.model.objects.get_or_create(id=1)
        return product_kitchen

class ListOrderView(AdminRequiredMixin, TemplateView):
    model = Order
    template_name = 'order/list.html'

class ListOrderViewJson(AjayDatatableView):
    model = Order
    columns = ['product','quantity','total_amount','status','created_at', 'actions']
    exclude_from_search_cloumn = ['actions']



    def render_column(self, row, column):
        if column == 'created_at':
            created_at = row.created_at
            return created_at.strftime("%d-%b-%Y %H:%M:%p")

        if column == 'status':
            if row.status == 'captured':
                return "Success"
            else:
                return row.status
        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-sm mr-1">Edit</a>'.format(
                reverse('order-edit', kwargs={'pk': row.pk}))
            return edit_action
        else:
            return super(ListOrderViewJson, self).render_column(row, column)


class UpdateOrderView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Order
    fields = ['first_name','phone','address','state','country','pincode','status']
    template_name = 'order/form.html'
    success_message = "Order has been updated successfully"
    success_url = reverse_lazy('order-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateOrderView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class DeleteOrderView(AdminRequiredMixin, DeleteView):
    model = Product

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)



class CreateTestimonialView(AdminRequiredMixin, SuccessMessageMixin, CreateView):

    model = Testimonial
    form_class = CreateTestimonialForm
    template_name = 'testimonial/form.html'
    success_message = "Testimonial has been created successfully"
    success_url = reverse_lazy('testimonial-list')
    object = None

    def get_form_kwargs(self):
        kwargs = super(CreateTestimonialView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, *args, **kwargs):

        form = self.form_class()
        return self.render_to_response(
            self.get_context_data(
                form=form,
            )
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save()
            messages.success(request, self.success_message)
        else:
            return render(request, self.template_name,
                          {'form': form })

        return HttpResponseRedirect(self.success_url)

#Testimonial
class ListTestimonialView(AdminRequiredMixin, TemplateView):
    model = Testimonial
    template_name = 'testimonial/list.html'


class ListTestimonialViewJson(AjayDatatableView):
    model = Testimonial
    columns = ['title', 'actions']
    exclude_from_search_cloumn = ['actions']

    def render_column(self, row, column):

        if column == 'actions':

            clone_action = '<a href={} role="button" class="btn btn-info btn-sm mr-1">Clone</a>'.format(
                reverse('testimonial-clone', kwargs={'pk': row.pk}))

            edit_action = '<a href={} role="button" class="confirm btn btn-warning btn-sm mr-1">Edit</a>'.format(
                reverse('testimonial-edit', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-sm" data-url={} role="button">Delete</a>'.format(
                reverse('testimonial-delete', kwargs={'pk': row.pk}))
            return edit_action + clone_action +  delete_action
        else:
            return super(ListTestimonialViewJson, self).render_column(row, column)


class UpdateTestimonialView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Testimonial
    form_class = CreateTestimonialForm
    template_name = 'testimonial/form.html'
    success_message = "Testimonial updated successfully"
    success_url = reverse_lazy('testimonial-list')

    def get(self, request, pk, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)

        return self.render_to_response(
            self.get_context_data(form=form,
                                  )
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(self.request.POST, self.request.FILES, instance=self.object)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  )
        )

class DeleteTestimonialView(AdminRequiredMixin, DeleteView):
    model = Testimonial

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)

class CloneTestimonialView(AdminRequiredMixin,View):
    def get(self,request,pk):
        print("HERE")
        print(pk)
        # Fetch the original object
        original_object = get_object_or_404(Testimonial, pk=pk)

        # Clone the object by setting its primary key to None
        original_object.pk = None
        original_object.title = original_object.title+"-Copy"
        original_object.save()

        # Redirect to the detail page of the cloned object (or anywhere else)
        return redirect('testimonial-edit', pk=original_object.pk)


#Trustee

class CreateTrusteeView(AdminRequiredMixin, SuccessMessageMixin, CreateView):

    model = Trustee
    form_class = CreateTrusteeForm
    template_name = 'trustee/form.html'
    success_message = "Trustee has been created successfully"
    success_url = reverse_lazy('trustee-list')
    object = None

    def get_form_kwargs(self):
        kwargs = super(CreateTrusteeView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, *args, **kwargs):

        form = self.form_class()
        return self.render_to_response(
            self.get_context_data(
                form=form,
            )
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save()
            messages.success(request, self.success_message)
        else:
            return render(request, self.template_name,
                          {'form': form })

        return HttpResponseRedirect(self.success_url)


class ListTrusteeView(AdminRequiredMixin, TemplateView):
    model = Trustee
    template_name = 'trustee/list.html'


class ListTrusteeViewJson(AjayDatatableView):
    model = Trustee
    columns = ['title', 'actions']
    exclude_from_search_cloumn = ['actions']

    def render_column(self, row, column):

        if column == 'actions':

            clone_action = '<a href={} role="button" class="btn btn-info btn-sm mr-1">Clone</a>'.format(
                reverse('trustee-clone', kwargs={'pk': row.pk}))

            edit_action = '<a href={} role="button" class="confirm btn btn-warning btn-sm mr-1">Edit</a>'.format(
                reverse('trustee-edit', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-sm" data-url={} role="button">Delete</a>'.format(
                reverse('trustee-delete', kwargs={'pk': row.pk}))
            return edit_action + clone_action +  delete_action
        else:
            return super(ListTrusteeViewJson, self).render_column(row, column)


class UpdateTrusteeView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Trustee
    form_class = CreateTrusteeForm
    template_name = 'trustee/form.html'
    success_message = "Trustee updated successfully"
    success_url = reverse_lazy('trustee-list')

    def get(self, request, pk, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)

        return self.render_to_response(
            self.get_context_data(form=form,
                                  )
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(self.request.POST, self.request.FILES, instance=self.object)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  )
        )

class DeleteTrusteeView(AdminRequiredMixin, DeleteView):
    model = Trustee

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)

class CloneTrusteeView(AdminRequiredMixin,View):
    def get(self,request,pk):
        print("HERE")
        print(pk)
        # Fetch the original object
        original_object = get_object_or_404(Trustee, pk=pk)

        # Clone the object by setting its primary key to None
        original_object.pk = None
        original_object.title = original_object.title+"-Copy"
        original_object.save()

        # Redirect to the detail page of the cloned object (or anywhere else)
        return redirect('trustee-edit', pk=original_object.pk)



#OurSupporter

class CreateOurSupporterView(AdminRequiredMixin, SuccessMessageMixin, CreateView):

    model = OurSupporter
    form_class = CreateOurSupporterForm
    template_name = 'our_supporter/form.html'
    success_message = "OurSupporter has been created successfully"
    success_url = reverse_lazy('our_supporter-list')
    object = None

    def get_form_kwargs(self):
        kwargs = super(CreateOurSupporterView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, *args, **kwargs):

        form = self.form_class()
        return self.render_to_response(
            self.get_context_data(
                form=form,
            )
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save()
            messages.success(request, self.success_message)
        else:
            return render(request, self.template_name,
                          {'form': form })

        return HttpResponseRedirect(self.success_url)


class ListOurSupporterView(AdminRequiredMixin, TemplateView):
    model = OurSupporter
    template_name = 'our_supporter/list.html'


class ListOurSupporterViewJson(AjayDatatableView):
    model = OurSupporter
    columns = ['title', 'actions']
    exclude_from_search_cloumn = ['actions']

    def render_column(self, row, column):

        if column == 'actions':

            clone_action = '<a href={} role="button" class="btn btn-info btn-sm mr-1">Clone</a>'.format(
                reverse('our_supporter-clone', kwargs={'pk': row.pk}))

            edit_action = '<a href={} role="button" class="confirm btn btn-warning btn-sm mr-1">Edit</a>'.format(
                reverse('our_supporter-edit', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-sm" data-url={} role="button">Delete</a>'.format(
                reverse('our_supporter-delete', kwargs={'pk': row.pk}))
            return edit_action + clone_action +  delete_action
        else:
            return super(ListOurSupporterViewJson, self).render_column(row, column)


class UpdateOurSupporterView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):

    model = OurSupporter
    form_class = CreateOurSupporterForm
    template_name = 'our_supporter/form.html'
    success_message = "OurSupporter updated successfully"
    success_url = reverse_lazy('our_supporter-list')

    def get(self, request, pk, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)

        return self.render_to_response(
            self.get_context_data(form=form,
                                  )
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(self.request.POST, self.request.FILES, instance=self.object)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  )
        )

class DeleteOurSupporterView(AdminRequiredMixin, DeleteView):
    model = OurSupporter

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)

class CloneOurSupporterView(AdminRequiredMixin,View):
    def get(self,request,pk):
        print("HERE")
        print(pk)
        # Fetch the original object
        original_object = get_object_or_404(OurSupporter, pk=pk)

        # Clone the object by setting its primary key to None
        original_object.pk = None
        original_object.title = original_object.title+"-Copy"
        original_object.save()

        # Redirect to the detail page of the cloned object (or anywhere else)
        return redirect('our_supporter-edit', pk=original_object.pk)



#Subscribers
class UpdateSubscriberView(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Subscription
    form_class = CreateSubscriberForm
    template_name = 'subscriber/form.html'
    success_message = "Subscriber updated successfully"
    success_url = reverse_lazy('subscriber-list')


class ListSubscriberView(AdminRequiredMixin, TemplateView):
    model = Subscription
    template_name = 'subscriber/list.html'


class ListSubscriberViewJson(AjayDatatableView):
    model = Subscription
    columns = ['name','phone_no','price','email','plan','is_active', 'actions']
    exclude_from_search_cloumn = ['actions']

    def get_initial_queryset(self):

        return self.model.objects.order_by('-created_at')

    def render_column(self, row, column):
        if column == 'name':
            return row.user.first_name
        if column == 'phone_no':
            return row.user.username
        if column == 'email':
            return row.user.email

        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-sm mr-1">Edit</a>'.format(
                reverse('subscriber-edit', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-sm" data-url={} role="button">Delete</a>'.format(
                reverse('subscriber-delete', kwargs={'pk': row.pk}))
            return edit_action + delete_action
        else:
            return super(ListSubscriberViewJson, self).render_column(row, column)


class DeleteSubscriberView(AdminRequiredMixin, DeleteView):
    model = Subscription

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)

#RazorPay plan
class ListRazorpayPlanView(AdminRequiredMixin, TemplateView):
    model = SubscriptionPlan
    template_name = 'razorpay/list.html'


class ListRazorpayPlanViewJson(AjayDatatableView):
    model = SubscriptionPlan
    columns = ['plan_id','name','price','is_active', 'actions']
    exclude_from_search_cloumn = ['actions']

    def render_column(self, row, column):

        if column == 'actions':
            if row.is_active:
                is_active_action = '<a href={} role="button" class="btn btn-danger btn-sm mr-1">Deactivate</a>'.format(
                    reverse('razorpay-plan-status', kwargs={'pk': row.pk}))
            else:
                is_active_action = '<a href={} role="button" class="btn btn-success btn-sm mr-1">Activate</a>'.format(
                    reverse('razorpay-plan-status', kwargs={'pk': row.pk}))
            return is_active_action
        else:
            return super(ListRazorpayPlanViewJson, self).render_column(row, column)


class RazorpayStatusView(AdminRequiredMixin,View):
    def get(self, request,pk):
        print(pk)

        plan_obj = SubscriptionPlan.objects.get(id=pk)
        print(plan_obj)
        if plan_obj.is_active:
            plan_obj.is_active = False
            plan_obj.save()
        else:
            plan_obj.is_active = True
            plan_obj.save()

        return HttpResponseRedirect(reverse_lazy('razorpay-plan-list'))


# Slider Modules

class CreateSliderView(AdminRequiredMixin, SuccessMessageMixin, CreateView):

    model = HomeSlider
    fields = ['title', 'type','amount','icon','main_image','description']
    template_name = 'slider/form.html'
    success_message = "%(title)s has been created successfully"
    success_url = reverse_lazy('slider-list')


class ListSliderView(AdminRequiredMixin, TemplateView):
    model = HomeSlider
    template_name = 'slider/list.html'

    def get_context_data(self, **kwargs):
        context = super(ListSliderView, self).get_context_data(**kwargs)
        context['slider'] = SLIDER_TYPE
        return context


class ListSliderViewJson(AjayDatatableView):
    model = HomeSlider
    columns = ['title','type', 'actions']
    exclude_from_search_cloumn = ['actions']

    def get_initial_queryset(self):
        print(self.request.GET)

        slider_type = self.request.GET.getlist('slider_type[]')

        filters_fileds = Q()
        if slider_type:
            slider_type = slider_type[0]
            filters_fileds.add(Q(type=slider_type), Q.AND)

        return self.model.objects.filter(filters_fileds).order_by('-created_at')

    def render_column(self, row, column):
        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-sm mr-1">Edit</a>'.format(
                reverse('slider-edit', kwargs={'pk': row.pk}))
            clone_action = '<a href={} role="button" class="btn btn-info btn-sm mr-1">Clone</a>'.format(
                reverse('slider-clone', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-sm" data-url={} role="button">Delete</a>'.format(
                reverse('slider-delete', kwargs={'pk': row.pk}))
            return edit_action + clone_action + delete_action
        else:
            return super(ListSliderViewJson, self).render_column(row, column)


class UpdateSliderView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):

    model = HomeSlider
    fields = ['title', 'type','amount','icon','main_image','description']
    template_name = 'slider/form.html'
    success_message = "%(title)s has been updated successfully"
    success_url = reverse_lazy('slider-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateSliderView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class DeleteSliderView(AdminRequiredMixin, DeleteView):
    model = HomeSlider

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)

class CloneSliderView(AdminRequiredMixin,View):
    def get(self,request,pk):
        print("HERE")
        print(pk)
        # Fetch the original object
        original_object = get_object_or_404(HomeSlider, pk=pk)

        # Clone the object by setting its primary key to None
        original_object.pk = None
        original_object.title = original_object.title+"-Copy"
        original_object.save()

        # Redirect to the detail page of the cloned object (or anywhere else)
        return redirect('slider-edit', pk=original_object.pk)
