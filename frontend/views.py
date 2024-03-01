import base64
import hashlib
import hmac
import json
import random
from datetime import time

import razorpay as razorpay
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string, get_template
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from paywix.payu import Payu
from rest_framework.generics import *
from rest_framework.generics import GenericAPIView
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView
from application.custom_classes import DevoteeRequiredMixin
from application.helper import send_contact_us
from application.settings.common import PAYU_CONFIG, RAZOR_PAY_ID, RAZOR_PAY_SECRET
from apps.front_app.models import Campaign, Mother, OurTeam, AboutUs, Distribution, DistributionImage, Setting, \
    AbandonCart
from apps.user.models import TransactionDetails
from frontend.forms import SetPasswordForm
from frontend.serializer import TransactionDetailsSerializer
from rest_framework.permissions import AllowAny

User = get_user_model()


class FrontendHomeView(View):
    def get(self, request):
        campaign_obj = Campaign.objects.all()
        # if request.user.is_authenticated:
        context = {
            'campaign_obj': campaign_obj
        }
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
        setting_obj = Setting.objects.first()
        send_contact_us(request,setting_obj.admin_email,context)
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
        campaign_obj = Campaign.objects.all().order_by('-created_at')
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
class UserLogoutView(DevoteeRequiredMixin, View):

    def get(self, request):
        logout(request)
        #return render(request, 'auth/login.html')
        return redirect('home')

# Save Abandon Cart
class AbandonView(View):

    def post(self, request):
        full_name = request.POST.get('full_name')
        mobile_no = request.POST.get('mobile_no')
        email = request.POST.get('email')
        abandon_obj = AbandonCart.objects.filter(mobile_no=mobile_no).first()
        if not abandon_obj:
            abandon_obj = AbandonCart()
            abandon_obj.full_name = full_name
            abandon_obj.mobile_no = mobile_no
            abandon_obj.email = email
            abandon_obj.save()

        response = {}
        return JsonResponse(response)


# Request 80G
class Request80GView(DevoteeRequiredMixin, View):

    def post(self, request):
        id = request.POST.get('transaction_id')
        pan_number = request.POST.get('pan_number')
        address = request.POST.get('address')
        transaction_obj = TransactionDetails.objects.get(id=id)
        transaction_obj.address1 = address
        transaction_obj.pan_number = pan_number
        transaction_obj.is_80g_request = True
        transaction_obj.save()
        #return render(request, 'auth/login.html')
        return redirect('my-donation')

class OngoingDevotionView(View):
    def get(self, request,id):
        compaign = Campaign.objects.get(slug=id)
        transaction_obj = TransactionDetails.objects.filter(status='success').order_by('-created_at')[:5]
        transaction_obj_20 = TransactionDetails.objects.filter(status='success').order_by('-created_at')[:20]
        context = {'compaign':compaign,'transaction_obj':transaction_obj,'transaction_obj_20':transaction_obj_20}
        return render(request, 'frontend/ongoing_devotion.html',context)


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

class FrontendProfileView(DevoteeRequiredMixin,View):
    def get(self, request):
        json_file_path = './cities_list.json'

        with open(json_file_path, 'r') as json_file:
            cities = json.load(json_file)

        context = {'cities':cities}
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

class FrontendDonationView(DevoteeRequiredMixin,View):
    def get(self, request):
        transaction_obj = TransactionDetails.objects.filter(phone=request.user.username)
        context = {'transaction_obj':transaction_obj}
        return render(request, 'frontend/donation.html', context)
#Thank you page
class FrontendThankYouView(DevoteeRequiredMixin,View):
    def get(self, request):
        form = SetPasswordForm()
        context = {'form':form}
        return render(request, 'frontend/thank_you.html', context)

class FrontendRazorThankYouView(DevoteeRequiredMixin,View):
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
        #if request.user.is_authenticated:
        context = {
            'html':html
        }
        return render(request, 'frontend/pay_page.html', context)


class FrontendRazorPayView(View):
    def post(self, request):
        # Create payu instance
        if request.POST.get('custom_check') == 'custom_check':
            amount = request.POST.get('ctm_amount')
        else:
            amount = request.POST.get('amount')


        order_id = initiate_payment(amount)
        payload = {
            'key': RAZOR_PAY_ID,
            'order_id': order_id,
            "amount": amount,
            "firstname": request.POST.get('first_name'),
            "email": request.POST.get('email'),
            "phone": request.POST.get('mobile_no'),
            "productinfo": request.POST.get('title'),
            "txnid": "OR_"+str(random.random()),
            "furl": PAYU_CONFIG['RESPONSE_URL_FAILURE'],
            "surl": PAYU_CONFIG['RESPONSE_URL_SUCCESS']
        }

        return render(request, 'frontend/razor_pay_page.html', payload)

class PayuSuccessAPIView(View):

    permission_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return HttpResponseRedirect(reverse('home'))

    def post(self, request):
        data = {k: v[0] for k, v in request.POST.lists()}

        # Instantiate your serializer manually
        serializer = TransactionDetailsSerializer(data=data)

        if serializer.is_valid():
            instance = serializer.save()
            user_obj = User.objects.filter(username=instance.phone).first()
            if not user_obj:
                email = instance.email if instance.email else ""
                user_obj = User.objects.create_user(first_name=instance.firstname, type='devotee',
                                                    username=instance.phone, email=email,
                                                    password=instance.phone)
                user_obj.save()
        else:
            # Handle serializer validation errors
            errors = serializer.errors
            return HttpResponseRedirect(reverse('home'))

        merchant_key = PAYU_CONFIG['merchant_key']
        merchant_salt = PAYU_CONFIG['merchant_salt']
        payu = Payu(merchant_key, merchant_salt, "live")

        if data['status'] == 'success':
            response = payu.check_transaction(**data)
            login(request, user_obj)
            return HttpResponseRedirect(reverse('thank-you'))
        else:
            return HttpResponseRedirect(reverse('home'))

class PayuFailureAPiView(GenericAPIView):

    """

       Class for creating API view for Payment Failure.

       """
    permission_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self,request):
        return HttpResponseRedirect(reverse('home', kwargs={}))

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

        return HttpResponseRedirect(reverse('home', kwargs={}))

def initiate_payment(amt):
    client = razorpay.Client(auth=(RAZOR_PAY_ID, RAZOR_PAY_SECRET))
    print(client)
    float_number = float(amt)

    # Convert float to integer
    amt = int(float_number)
    data = {
        'amount': amt * 100,  # Razorpay expects amount in paise (e.g., 100 INR = 10000 paise)
        'currency': 'INR',
        'payment_capture': '1'  # Auto capture the payment after successful authorization
    }
    response = client.order.create(data=data)
    return response['id']

@csrf_exempt
def payment_success_view(request):
   order_id = request.POST.get('order_id')
   payment_id = request.POST.get('razorpay_payment_id')
   # headers = request.headers
   # cookie_header = headers.get('Cookie', '')
   # cookies = cookie_header.split('; ')
   sessionid = None

   # for cookie in cookies:
   #     name, value = cookie.split('=')
   #     if name.strip() == 'sessionid':
   #         sessionid = value.strip()
   #         break
   # if request.COOKIES.get('sessionid') != sessionid:
   #     return HttpResponseRedirect(reverse('home'))

   client = razorpay.Client(auth=(RAZOR_PAY_ID, RAZOR_PAY_SECRET))
   try:
       res_data=client.order.payments(order_id)
       dic_data = res_data['items'][0]
       first_name = dic_data['email']
       email = dic_data['email']
       phone = dic_data['contact']
       phone = phone.replace("+91", "")

       user_obj = User.objects.filter(username=phone).first()
       if not user_obj:
           user_obj = User.objects.create_user(first_name=first_name, type='devotee',
                                               username=phone, email=email,
                                               password=phone)
           user_obj.save()
       pay_id = dic_data['id']
       amt = dic_data['amount']/100
       method = dic_data['method']
       status = dic_data['status']
       description = dic_data['description']
       tran_detail_obj = TransactionDetails()
       tran_detail_obj.mihpayid = pay_id
       tran_detail_obj.mode = method
       tran_detail_obj.productinfo = description
       tran_detail_obj.payment_source = method
       tran_detail_obj.amount = amt
       tran_detail_obj.status = status
       tran_detail_obj.email = email
       tran_detail_obj.phone = phone
       tran_detail_obj.save()
       print(dic_data)
       login(request, user_obj)
       return HttpResponseRedirect(reverse('thank-you-rj'))

   except razorpay.errors.SignatureVerificationError as e:

       return HttpResponseRedirect(reverse('home'))


def validate_signature(body, signature):
    # Get your Razorpay secret key
    razorpay_secret_key = 'YOUR_RAZORPAY_SECRET_KEY'

    # Calculate HMAC SHA256 hash of the request body
    expected_signature = hmac.new(razorpay_secret_key.encode(), body, hashlib.sha256).hexdigest()

    # Encode the expected signature in base64
    expected_signature = base64.b64encode(expected_signature.encode()).decode()
    print(expected_signature)

    # Compare the calculated signature with the signature received in the request
    return hmac.compare_digest(expected_signature, signature)


def handle_payment_webhook(request):
    # Verify webhook signature (optional but recommended)
    # ...

    # Parse webhook event
    payload = request.POST

    # Handle payment success event
    if payload['event'] == 'payment.captured':
        payment_id = payload['payload']['payment']['entity']['id']
        # Update your database with payment success status
        # ...

    return JsonResponse({'status': 'success'})

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


class Download80gView(DevoteeRequiredMixin,View):
    def get(self, request,id):
        # Get the HTML template
        transaction_obj = TransactionDetails.objects.get(id=id)
        return render(request, 'frontend/invoice_80g.html', {'transaction_obj':transaction_obj})


def forgot_password(request,token=''):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri('/reset-password/{}/'.format(token))
            s = send_mail('Password Reset', 'Click the link to reset your password: {}'.format(reset_link), 'contact@thepuredevotion.in', [email])
            print("Test", s)
        return redirect('password_reset_done')
    return render(request, 'frontend/forgot_password.html')

def reset_password(request, token):
    # Handle password reset logic here
    pass

