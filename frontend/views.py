from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView
from application.custom_classes import AjayDatatableView, StudentRequiredMixin
from application.helper import send_contact_us
from apps.front_app.models import Campaign, Mother, OurTeam, AboutUs

User = get_user_model()


class FrontendHomeView(View):
    def get(self, request):

        #if request.user.is_authenticated:
        context = {}
        return render(request, 'frontend/home.html', context)

class FrontendAboutUsView(View):
    def get(self, request):
        ourteam_obj = OurTeam.objects.all()
        about_obj = AboutUs.objects.first()
        # if request.user.is_authenticated:
        context = {
            'ourteam_obj': ourteam_obj,
            'about_obj':about_obj,
        }

        return render(request, 'frontend/about-us.html', context)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile_no')
        message = request.POST.get('message')
        context = {
            'first_name':first_name,
            'last_name': last_name,
            'email': email,
            'mobile_no': mobile_no,
            'message': message
        }
        send_contact_us(request,['bhavanshu@icloud.com'],context)
        url = reverse('about-us', kwargs={})

        return HttpResponseRedirect(url)



class FrontendOurMotherView(View):
    def get(self, request):
        mother_obj = Mother.objects.all()
        #if request.user.is_authenticated:
        context = {
            'mother_obj':mother_obj
        }
        return render(request, 'frontend/our_mother.html', context)


class FrontendCampaignView(View):
    def get(self, request):
        campaign_obj = Campaign.objects.all()
        #if request.user.is_authenticated:
        context = {
            'campaign_obj':campaign_obj
        }
        return render(request, 'frontend/campaign.html', context)

class FrontendDistributionView(View):
    def get(self, request):

        #if request.user.is_authenticated:
        context = {}
        return render(request, 'frontend/distribution.html', context)

class FrontendPrivacyPolicyView(View):
    def get(self, request):

        #if request.user.is_authenticated:
        context = {}
        return render(request, 'frontend/privacy_policy.html', context)


class FrontendTermConditionView(View):
    def get(self, request):

        #if request.user.is_authenticated:
        context = {}
        return render(request, 'frontend/term_condition.html', context)



class FrontendRefundPolicyView(View):
    def get(self, request):

        #if request.user.is_authenticated:
        context = {}
        return render(request, 'frontend/refund_policy.html', context)