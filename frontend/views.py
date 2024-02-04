import random

from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from paywix.payu import Payu
from rest_framework.generics import *
from rest_framework.generics import GenericAPIView
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView
from application.custom_classes import AjayDatatableView, StudentRequiredMixin
from application.helper import send_contact_us
from application.settings.common import PAYU_CONFIG
from apps.front_app.models import Campaign, Mother, OurTeam, AboutUs, Distribution, DistributionImage
from apps.user.models import TransactionDetails
from frontend.forms import SetPasswordForm
from frontend.serializer import TransactionDetailsSerializer

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
        distribution_obj = Distribution.objects.all()
        unique_years_queryset = Distribution.objects.dates('date', 'year', order='DESC')

        # Extract the years from the queryset
        unique_years_list = [entry.year for entry in unique_years_queryset]

        context = {'distribution_obj': distribution_obj, 'unique_years_list': unique_years_list}
        return render(request, 'frontend/distribution.html', context)

    def post(self, request):
        month = request.POST.get('month')
        year = request.POST.get('year')
        distribution_obj = Distribution.objects.filter(date__month=month, date__year=year)
        distribution_html = render_to_string('frontend/distribution_html.html',
                                             {'distribution_obj': distribution_obj})
        payload = {
            'distribution_html': distribution_html,
            'success': 'ok',
        }
        return JsonResponse(payload, safe=False)



class FrontendDistributionDetailView(View):
    def get(self, request,pk):
        distribution_obj = Distribution.objects.get(id=pk)

        distribution_detail_obj = DistributionImage.objects.filter(distribution=pk)
        #if request.user.is_authenticated:
        context = {'distribution_detail_obj':distribution_detail_obj,'distribution_obj':distribution_obj}
        return render(request, 'frontend/distribution_detail.html', context)


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

#Logout page
class UserLogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        #return render(request, 'auth/login.html')
        return redirect('home')


# Login page
class FrontendLoginView(View):
    login_url = 'user-login'
    success_message = 'You have successfully logged in.'
    failure_message = 'Sorry, unrecognized username or password. Have you forgotten your password?.'

    def get(self, request):
        context = {}
        return render(request, 'frontend/login.html', context)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Password", password)
        kwargs = {'username__iexact': username}
        try:
            user = get_user_model().objects.get(**kwargs)
            print(user)
            if not user.check_password(password):
                print("Not auth")
                messages.error(request, self.failure_message)
                return HttpResponseRedirect(reverse(self.login_url))
        except User.DoesNotExist:
            messages.error(request, self.failure_message)
            return HttpResponseRedirect(reverse(self.login_url))

        user = authenticate(request, username=username,
                            password=password)
        login(request, user)
        if user:
            return HttpResponseRedirect(reverse('home', kwargs={}))
# My profile page

class FrontendProfileView(View):
    def get(self, request):
        context = {}
        return render(request, 'frontend/profile.html', context)

    def post(self,request):
        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        user = User.objects.get(id=request.user.id)
        user.address = address
        user.city = city
        user.pincode = pincode
        user.save()

        return HttpResponseRedirect(reverse('profile', kwargs={}))
# My donation page

class FrontendDonationView(View):
    def get(self, request):
        transaction_obj = TransactionDetails.objects.filter(phone=request.user.username)
        context = {'transaction_obj':transaction_obj}
        return render(request, 'frontend/donation.html', context)
#Thank you page
class FrontendThankYouView(View):
    def get(self, request):
        form = SetPasswordForm()
        context = {'form':form}
        return render(request, 'frontend/thank_you.html', context)

# Payment gateway
class FrontendPayView(View):
    def post(self, request):
        # Create payu instance
        if request.POST.get('custom_check') == 'custom_check':
            amount = request.POST.get('ctm_amount')
        else:
            amount = request.POST.get('amount')

        merchant_key = PAYU_CONFIG['merchant_key']
        merchant_salt = PAYU_CONFIG['merchant_salt']
        payu = Payu(merchant_key, merchant_salt, "live")
        payload = {
            "amount": amount,
            "firstname": request.POST.get('first_name'),
            "email": request.POST.get('email'),
            "phone": request.POST.get('mobile_no'),
            "productinfo": request.POST.get('title'),
            "txnid": "OR_"+str(random.random()),
            "furl": PAYU_CONFIG['RESPONSE_URL_FAILURE'],
            "surl": PAYU_CONFIG['RESPONSE_URL_SUCCESS']
        }

        response = payu.transaction(**payload)
        html = payu.make_html(response)
        print(html)
        #if request.user.is_authenticated:
        context = {
            'html':html
        }
        return render(request, 'frontend/pay_page.html', context)


class PayuSuccessAPiView(GenericAPIView):

    """

       Class for creating API view for Payment Success.

       """

    serializer_class = TransactionDetailsSerializer


    def post(self, request):

        """

        Function for Payment Success.

        """

        serializer = self.get_serializer(data=request.data)

        data = {k: v[0] for k, v in dict(request.data).items()}

        if serializer.is_valid():
            instance = serializer.save()
            user_obj = User.objects.filter(username=instance.phone).first()
            if not user_obj:
                user_obj = User.objects.create_user(first_name=instance.firstname,type='devotee',username=instance.phone, email='bhavanshu@icloud.com',
                                               password=instance.phone)
                user_obj.save()


            print(f"Saved instance: {instance}")
        else:
            errors = serializer.errors

            return HttpResponseRedirect(reverse('home', kwargs={}))


        merchant_key = PAYU_CONFIG['merchant_key']
        merchant_salt = PAYU_CONFIG['merchant_salt']
        payu = Payu(merchant_key, merchant_salt, "live")
        if data['status'] == 'success':
            response = payu.check_transaction(**data)
            login(request,user_obj)
            return HttpResponseRedirect(reverse('thank-you', kwargs={}))
        else:
            return HttpResponseRedirect(reverse('home', kwargs={}))


class PayuFailureAPiView(GenericAPIView):

    """

       Class for creating API view for Payment Failure.

       """


    @csrf_exempt

    def post(self, request):

        """

        Function for Payment Failure.

        """

        data = {k: v[0] for k, v in dict(request.data).items()}
        merchant_key = PAYU_CONFIG['merchant_key']
        merchant_salt = PAYU_CONFIG['merchant_salt']
        payu = Payu(merchant_key, merchant_salt, "live")
        response = payu.verify_transaction(data)

        return JsonResponse(response)

@login_required
def set_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            password = form.cleaned_data['password']
            user.set_password(password)
            user.is_password_save = True
            user.save()
            messages.success(request, 'Password set successfully.')
            return redirect('thank-you')  # Redirect to the user's profile page or wherever you want
    else:
        form = SetPasswordForm()

    return render(request, 'frontend/thank_you.html', {'form': form})