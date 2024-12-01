import base64
import hashlib
import hmac
import json
import random
import datetime
import time
import uuid
from datetime import datetime, timedelta
from django.utils.html import strip_tags  # For generating plain text fallback

import razorpay as razorpay
import requests
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string, get_template
from django.utils.crypto import get_random_string
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
from application.custom_classes import DevoteeRequiredMixin, AdminRequiredMixin, AjayDatatableView
from application.email_helper import send_email_background, send_email
from application.helper import send_contact_us, write_log, send_whatsapp_message, send_donation_thank_you_email
from application.settings.common import PAYU_CONFIG, RAZOR_PAY_ID, RAZOR_PAY_SECRET, ADMIN_EMAIL
from apps.front_app.forms import CreateTestimonialForm
from apps.front_app.models import Campaign, Mother, OurTeam, AboutUs, Distribution, DistributionImage, Setting, \
    AbandonCart, Testimonial, CampaignProduct, Product, Trustee, OurSupporter, UploadedFile, Gallery, AdoptedCow, \
    HomeSlider, Order
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core import serializers

from apps.promoter.models import Promoter
from apps.user.models import TransactionDetails, OTP, SubscriptionPlan, ProductItemTrans, Subscription
from frontend.forms import SetPasswordForm, VerifyOTPForm
from frontend.serializer import TransactionDetailsSerializer
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.conf import settings
User = get_user_model()


razorpay_client = razorpay.Client(auth=(settings.RAZOR_PAY_ID, settings.RAZOR_PAY_SECRET))


class FrontendHomeView(View):
    def get(self, request):
        campaign_obj = Campaign.objects.all()
        monthly_campaign_obj = Campaign.objects.filter(type='Seva',mode='One Time')
        home_campaign_obj = Campaign.objects.filter(is_home=True).exclude(Q(type='Seva') | Q(type='Adopt a cow'))
        testimonial_obj = Testimonial.objects.all()
        gallery_obj = Distribution.objects.all()
        # if request.user.is_authenticated:
        context = {
            'gallery_obj':gallery_obj,
            'campaign_obj': campaign_obj,
            'testimonial_obj':testimonial_obj,
            'home_campaign_obj':home_campaign_obj,
            'monthly_campaign_obj':monthly_campaign_obj,
        }
        return render(request, 'frontend/home.html', context)

class FrontendAboutUsView(View):
    def get(self, request):
        ourteam_obj = OurTeam.objects.all()
        about_obj = AboutUs.objects.first()
        gallery_obj = Distribution.objects.all()
        about_1 = HomeSlider.objects.filter(type='About 1')
        about_2 = HomeSlider.objects.filter(type='About 2')
        # if request.user.is_authenticated:
        context = {
            'about_1':about_1,
            'about_2':about_2,
            'gallery_obj':gallery_obj,
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


class FrontendTrusteeView(View):
    def get(self, request):

        trustree_obj = Trustee.objects.all().order_by('order_number')
        # if request.user.is_authenticated:
        context = {
            'trustree_obj':trustree_obj
        }

        return render(request, 'frontend/trustee.html', context)



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
        subscription_obj = Subscription.objects.filter(is_active=True)

        campaign_list = subscription_obj.values_list('campaign_id', flat=True)

        adopt_a_cow_obj = Campaign.objects.filter(type='Adopt a cow').exclude(id__in=campaign_list).order_by('-created_at')
        campaign_obj = Campaign.objects.exclude(type='Adopt a cow').exclude(type='Seva').order_by('-created_at')

        gallery_obj = Distribution.objects.all()
        product_obj = Product.objects.all()
        #if request.user.is_authenticated:
        context = {
            'gallery_obj':gallery_obj,
            'campaign_obj':campaign_obj,
            'adopt_a_cow_obj':adopt_a_cow_obj,
            'product_obj':product_obj
        }
        return render(request, 'frontend/campaign.html', context)

class FrontendDistributionView(View):
    def get(self, request):
        distribution_obj = Distribution.objects.all()
        unique_years_queryset = Distribution.objects.dates('date', 'year', order='DESC')

        # Extract the years from the queryset
        unique_years_list = [entry.year for entry in unique_years_queryset]

        context = {'distribution_obj': distribution_obj, 'unique_years_list': unique_years_list}
        return render(request, 'frontend/gallery.html', context)

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
        distribution_detail_obj = UploadedFile.objects.filter(uploader_id=pk)
        #if request.user.is_authenticated:
        context = {'distribution_detail_obj':distribution_detail_obj}
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


class GetCampaignView(DevoteeRequiredMixin, View):

    def get(self, request,pk):
        campaign_single = Campaign.objects.get(id=pk)

        response = {'description': campaign_single.description,'title': campaign_single.title}
        return JsonResponse(response)


class AdoptedCowView(View):
    def get(self, request):
        campaign_ids = Campaign.objects.filter(type='Adopt a cow').values_list('id', flat=True)
        subscription_obj = Subscription.objects.filter(is_active=True)
        campaign_list = subscription_obj.values_list('campaign_id', flat=True)
        campaigns_data = []
        adopted_cow = Campaign.objects.filter(type='Adopt a cow',is_active=True).exclude(id__in=campaign_list)

        context = {
            'waiting_cow_len': len(adopted_cow),
            'adopted_cow_len': len(subscription_obj),
            'subscription_obj':subscription_obj,
        }
        return render(request, 'frontend/adopted_cow.html', context)


class WaitingCowView(ListView):
    def get(self, request):

        campaign_ids = Campaign.objects.filter(type='Adopt a cow').values_list('id', flat=True)
        adopted_ids = AdoptedCow.objects.values_list('campaign_id', flat=True)

        campaigns_data = []
        adopted_cow = AdoptedCow.objects.filter(campaign_id__in=campaign_ids, is_active=True)

        subscription_obj = Subscription.objects.filter(is_active=True)

        campaign_list = subscription_obj.values_list('campaign_id', flat=True)
        campaigns_data = []
        adopted_cow = Campaign.objects.filter(type='Adopt a cow', is_active=True).exclude(id__in=campaign_list)

        waiting_cow_obj = Campaign.objects.filter(type='Adopt a cow').exclude(id__in=campaign_list)


        # Pagination
        paginator = Paginator(waiting_cow_obj, 20)  # 5 items per page
        page = request.GET.get('page')

        try:
            waiting_cow_paginated = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            waiting_cow_paginated = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            waiting_cow_paginated = paginator.page(paginator.num_pages)


        context = {
            'waiting_cow_len': len(adopted_cow),
            'adopted_cow_len': len(subscription_obj),
            'adopted_cow': adopted_cow,
            'waiting_cow_paginated':waiting_cow_obj
        }
        return render(request, 'frontend/waiting_cow.html', context)


class OurSupportersView(View):
    def get(self, request):
        our_supporter_obj = OurSupporter.objects.all()
        context = {
            'our_supporter_obj':our_supporter_obj
        }
        return render(request, 'frontend/our_supporters.html', context)

class OurSupporterDetailView(View):
    def get(self, request,id):
        our_supporter_obj = OurSupporter.objects.get(id=id)
        context = {
            'our_supporter_obj':our_supporter_obj
        }
        return render(request, 'frontend/our_supporter_detail.html', context)

class GalleryView(View):
    def get(self, request):
        context = {}
        return render(request, 'frontend/gallery.html', context)

class SevaView(View):
    def get(self, request):
        context = {}
        return render(request, 'frontend/seva.html', context)

class ProductView(View):
    def get(self, request):
        product_obj = Product.objects.all()

        context = {
            'product_obj':product_obj
        }
        return render(request, 'frontend/product.html', context)

class CsrView(View):
    def get(self, request):

        context = {}
        return render(request, 'frontend/csr.html', context)

    def post(self, request):
        print("HERE IT CAME")
        full_name = request.POST.get('name')
        mobile_no = request.POST.get('mobile_no')
        designation = request.POST.get('designation')
        company_name = request.POST.get('company_name')
        full_address = request.POST.get('full_address')
        email = request.POST.get('email')
        template = 'frontend/email/csr_template.html'

        context = {
            'name':full_name,
            'mobile_no': mobile_no,
            'email': email,
            'designation':designation,
            'company_name':company_name,
            'full_address':full_address,

        }
        send_email_background(request, ADMIN_EMAIL, template, context, subject='CSR Request')
        messages.success(self.request, "Thanks you, we will get back to you")

        return redirect('csr')

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


class SendCSRView(DevoteeRequiredMixin, View):

    def post(self, request):
        template = 'frontend/email/event_admin_template.html'
        context = {
            'name': request.POST.get('name'),
            'mobile_no': request.POST.get('mobile_no'),
            'email': request.POST.get('email'),
            'message': request.POST.get('message'),
            'for_vi': request.POST.get('for'),
            'schedule_date': request.POST.get('schedule_date'),
        }
        setting_obj = Setting.objects.first()
        send_email_background(request, setting_obj.admin_email, template, context, subject='New Notification')
        messages.success(request, "Thank you for submitting ")

        return redirect('home')
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

class OngoingDevotionPromoView(ListView):
    def get(self, request, id, promo_no):
        promo_obj = Promoter.objects.filter(promoter_no=promo_no).first()
        if not promo_obj:
            return redirect('home')
        compaign = Campaign.objects.get(slug=id)
        transaction_obj = TransactionDetails.objects.filter(Q(status='success') | Q(status='captured')).order_by('-created_at')

        # Pagination
        paginator = Paginator(transaction_obj, 20)  # 5 items per page
        page = request.GET.get('page')

        try:
            transaction_obj_paginated = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            transaction_obj_paginated = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            transaction_obj_paginated = paginator.page(paginator.num_pages)

        context = {'promo_no':promo_no,'compaign': compaign, 'transaction_obj_paginated': transaction_obj_paginated}
        return render(request, 'frontend/ongoing_devotion.html', context)

class GetCampaignProductView(View):
    def post(self, request):
        id = request.POST.get('id')
        campaign_product = Campaign.objects.get(id=id)
        if campaign_product.product:
            campaign_with_product_html = render_to_string('frontend/campaign_with_product_html.html',
                                                 {'campaign': campaign_product,'campaign_product': campaign_product})
        else:
            campaign_with_product_html = ""
        payload = {
            'campaign_with_product_html': campaign_with_product_html,
            'success': 'ok',
        }
        return JsonResponse(payload, safe=False)


def get_campaign(identifier):
    campaign_obj = get_object_or_404(Campaign, Q(slug=identifier) | Q(id=identifier))
    return campaign_obj


class OngoingDevotionView(ListView):
    def get(self, request, id):

        campaign_obj = Campaign.objects.get(slug=id)
        print("HERE")
        print(campaign_obj)
        transaction_obj = TransactionDetails.objects.filter(Q(status='success') | Q(status='captured')).order_by('-created_at')

        # Pagination
        paginator = Paginator(transaction_obj, 20)  # 5 items per page
        page = request.GET.get('page')

        try:
            transaction_obj_paginated = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            transaction_obj_paginated = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            transaction_obj_paginated = paginator.page(paginator.num_pages)

        context = {'campaign': campaign_obj, 'transaction_obj_paginated': transaction_obj_paginated}
        return render(request, 'frontend/ongoing_devotion.html', context)


# Login page
class FrontendLoginView(View):
    login_url = 'user-login'
    success_message = 'You have successfully logged in.'
    failure_message = 'Sorry, unrecognized username or password. Have you forgotten your password?.'

    def get(self, request):
        context = {}
        return render(request, 'frontend/login.html', context)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("Password", password)

        kwargs = {'email__iexact': email}
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

        user = authenticate(request, username=email,
                            password=password)
        print("User")
        print(user)
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
        mobile_no = request.POST.get('mobile_no')
        profile = request.FILES.get('profile')
        name = request.POST.get('name')
        user = User.objects.get(id=request.user.id)
        user.address = address
        user.mobile_no = mobile_no
        user.first_name = name
        if profile:
            user.profile = profile
        user.save()
        messages.success(request, 'Profile has been updated successfully')

        return HttpResponseRedirect(reverse('my-donation', kwargs={}))
# My donation page


class FrontendDonationView(DevoteeRequiredMixin,View):
    def get(self, request):
        transaction_obj = TransactionDetails.objects.filter(Q(phone=request.user.username) | Q(email=request.user.email))
        context = {'transaction_obj':transaction_obj}
        return render(request, 'frontend/donation.html', context)


#Thank you page
class FrontendThankYouView(DevoteeRequiredMixin,View):
    def get(self, request):
        form = SetPasswordForm()
        context = {'form':form}

        return render(request, 'frontend/thank_you.html', context)


class FrontendRazorThankYouView(View):
    def get(self, request,id):
        form = SetPasswordForm()
        context = {'form':form,'id':id}
        return render(request, 'frontend/thank_you.html', context)


# Donate Monthly
class DonateMontlyView(ListView):
    def get(self, request, id):
        campaign = Campaign.objects.get(slug=id)
        subscription_plan = SubscriptionPlan.objects.filter(is_active=True)
        if campaign.type == 'Adopt a cow':
            adopt_a_cow = True
            plan_id = "plan_OpIeG90yIMyKEI"
        else:
            adopt_a_cow = False
            plan_id = ""

        order_data = {
            "amount": 50000,  # Amount in paise
            "currency": "INR",
            "receipt": "receipt#1",
            "payment_capture": 1  # Auto-capture the payment
        }

        order = razorpay_client.order.create(data=order_data)


        context = {'plan_id':plan_id,'adopt_a_cow':adopt_a_cow, 'razorpay_key_id': settings.RAZOR_PAY_ID,'order': order,'campaign': campaign,'subscription_plan':subscription_plan }
        return render(request, 'frontend/donate_monthly.html', context)


class DonateMontlyCtmView(ListView):
    def get(self, request):
        campaign_slug = request.GET.get('campaign_slug')
        if campaign_slug:
            campaign = Campaign.objects.filter(slug=campaign_slug).first()
        else:
            campaign = Campaign.objects.filter(type='Seva').first()
        price = request.GET.get('amount')
        preferred_date = request.GET.get('preferred_date')
        first_name = request.GET.get('first_name')
        email = request.GET.get('email')
        phone_no = request.GET.get('phone_no')
        subscription_plan = SubscriptionPlan.objects.filter(is_active=True)
        if campaign.type == 'Adopt a cow':
            adopt_a_cow = True
            plan_id = "plan_OpIeG90yIMyKEI"
        else:
            adopt_a_cow = False
            plan_id = ""

        if price:
            plan_id = "plan_OpIeG90yIMyKEI"

        order_data = {
            "amount": 50000,  # Amount in paise
            "currency": "INR",
            "receipt": "receipt#1",
            "payment_capture": 1  # Auto-capture the payment
        }

        order = razorpay_client.order.create(data=order_data)

        print(price)
        context = {'phone_no':phone_no,'first_name':first_name,'email': email,'preferred_date':preferred_date,'price':price,'plan_id':plan_id,'adopt_a_cow':adopt_a_cow, 'razorpay_key_id': settings.RAZOR_PAY_ID,'order': order,'campaign': campaign,'subscription_plan':subscription_plan }
        return render(request, 'frontend/donate_monthly.html', context)


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

@method_decorator(csrf_exempt, name='dispatch')
class FrontendRazorPayView(View):
    def post(self, request):
        # Create payu instance:
        if request.POST.get('ctm_amount'):
            amount = request.POST.get('ctm_amount')
        else:
            print("Direct amt")
            amount = request.POST.get('amount')
        print("amount")
        print(amount)
        if request.POST.get('phone'):
            phone = request.POST.get('phone')
        else:
            phone = request.POST.get('mobile_no')
        if request.POST.get('type') == 'product':
            # Retrieve form data
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            country = request.POST['country']
            state = request.POST['state']
            print("country"+ country)
            print("Stat", state)
            pincode = request.POST['pincode']
            address = request.POST['address']
            comment = request.POST.get('comment', '')
            product_name = request.POST.get('product_name', '')

            product_id = request.POST.get('product_id', None)
            quantity = request.POST.get('quantity', 1)

            # Calculate total_amount based on the product and quantity
            product = Product.objects.get(id=product_id) if product_id else None

            total_amount = product.price * int(quantity) if product else 0.0
            amount = request.POST.get('total_price')
            # Create and save the order
            order = Order(
                product_name=product_name,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                product=product,
                address=address,
                comment=comment,
                country=country,
                pincode=pincode,
                state=state,
                quantity=quantity,
                total_amount=amount,
                payment_method='',
                payment_status='',
                discount=0.0,
                tax=0.0,
                notes='',
                tracking_number='',
                status='pending'
            )

            order.save()
        else:
            multiple_campaign = request.POST.get('multiple_campaign', '')


        campaign_id = request.POST.get('campaign_id')
        if campaign_id:
            slug = Campaign.objects.get(id=campaign_id).slug
        else:
            slug = ""
        tip = request.POST.get('tip')
        city = request.POST.get('city')
        all_item_data = request.POST.get('all_item_data')

        if tip:
            tip = float(tip)
        else:
            tip = 0

        order_id = initiate_payment(amount,request.POST.get('first_name'),request.POST.get('email'),phone,tip,city)

        if all_item_data:
            my_object = json.loads(all_item_data)
            for single in my_object:
                print(single)
                prod_obj = CampaignProduct.objects.get(id=single['id'])
                prod_item = ProductItemTrans()
                prod_item.order_id = order_id
                prod_item.quantity = single['count']
                prod_item.product = prod_obj
                prod_item.save()


        payload = {
            'key': RAZOR_PAY_ID,
            'order_id': order_id,
            "amount": amount,
            "firstname": request.POST.get('first_name'),
            "email": request.POST.get('email'),
            "phone": request.POST.get('mobile_no'),
            'custom_campaign_id': campaign_id,
            'tip': tip,
            'slug':slug,
            'multiple_campaign':multiple_campaign,
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


def create_user(name,email,password,phone='',type='devotee',city=''):
    additional_data = {
        'first_name': name,
        'last_name': '',
        'mobile_no': phone,
        'city': city,
        'plain_password': password,  # Store plaintext for initial email; avoid this for security-sensitive use
    }

    # Create or get the user with the specified parameters
    user_obj, created = User.objects.get_or_create(
        email=email,
        defaults={
            **additional_data,
            'type': type,
        }
    )

    # If created, set the password securely
    if created:
        user_obj.set_password(password)
        user_obj.save()

    return user_obj

def initiate_payment(amt,name,email,phone,tip,city):
    client = razorpay.Client(auth=(RAZOR_PAY_ID, RAZOR_PAY_SECRET))
    print(client)
    float_number = float(amt)

    # Convert float to integer
    amt = int(float_number)
    data = {
        'amount': amt * 100,  # Razorpay expects amount in paise (e.g., 100 INR = 10000 paise)
        'currency': 'INR',
        'notes': {
            'firstname': name,
            'email': email,
            'contact': phone,
            'city': city
        },
        'payment_capture': '1'  # Auto capture the payment after successful authorization
    }
    response = client.order.create(data=data)
    tran_obj = TransactionDetails()
    tran_obj.order_id = response['id']
    tran_obj.status = 'pending'
    tran_obj.amount = 0
    tran_obj.tip = tip
    tran_obj.save()
    return response['id']

@csrf_exempt
def payment_success_view(request):
   write_log("ALl POST DATA ORDER", request.POST.dict())
   order_id = request.POST.get('order_id')
   write_log("Order id", order_id)
   payment_id = request.POST.get('razorpay_payment_id')

   client = razorpay.Client(auth=(RAZOR_PAY_ID, RAZOR_PAY_SECRET))
   try:
       res_data=client.order.payments(order_id)
       write_log("Order details", res_data)
       dic_data = res_data['items'][0]
       print(dic_data)
       if dic_data['status'] != 'failed':
           write_log("Order details single", dic_data)
           first_name = dic_data['notes']['firstname']
           city = dic_data['notes']['city']

           email = dic_data['email']
           phone = dic_data['contact']
           phone = phone.replace("+91", "")
           write_log("Order notes",dic_data['notes'])
           password = uuid.uuid4()
           user_obj = create_user(first_name,email,password,phone,'devotee', city)

           write_log("User create for ", email)

           custom_campaign_id = dic_data['notes']['custom_campaign_id']

           pay_id = dic_data['id']
           amt = dic_data['amount']/100
           method = dic_data['method']
           status = dic_data['status']
           description = dic_data['description']
           tran_detail_obj = TransactionDetails.objects.filter(order_id=order_id).first()
           if not tran_detail_obj:
               tran_detail_obj = TransactionDetails()

           try:
               multiple_campaign = dic_data['notes']['multiple_campaign']
               tran_detail_obj.field1 = multiple_campaign
           except Exception as e:
               pass

           tran_detail_obj.mihpayid = pay_id
           tran_detail_obj.order_id = order_id
           tran_detail_obj.mode = method
           tran_detail_obj.firstname = first_name
           tran_detail_obj.productinfo = description
           tran_detail_obj.payment_source = method
           if custom_campaign_id:
               tran_detail_obj.campaign_id = custom_campaign_id

           tran_detail_obj.amount = float(amt)
           tran_detail_obj.status = status
           tran_detail_obj.email = email
           tran_detail_obj.phone = phone
           tran_detail_obj.save()
           write_log("Transation created for ", email)
           write_log("Transaction no", tran_detail_obj.id)

           receipt_url = settings.BASE_URL+"/receipt/"+str(tran_detail_obj.id)
           send_donation_thank_you_email(first_name, email, float(amt), receipt_url)
           write_log("Message send for ", email)
           #login(request, user_obj)

           invoice_link = settings.BASE_URL+str(tran_detail_obj.id)
           message = (
               f"🕉️ *Hingonia* 🕉️\n\n"
               f"Dear {first_name},\n\n"
               "🙏 *Thank you for your generous donation!* 🙏\n\n"
               "We are truly grateful for your support towards our mission. "
               f"Your contribution of ₹{amt} will go a long way in supporting our cause and making a positive impact.\n\n"
               "You can download your invoice from the following link:\n"
               f"{invoice_link}\n\n"  # Add the invoice link dynamically
               "If you have any queries or would like to stay updated on our activities, "
               "feel free to contact us at +91 9112524911 or visit our website.\n\n"
               "May Lord Shiva's blessings be with you always.\n\n"
               "*Om Namah Shivaya* 🙏\n\n"
               "Hingonia"
           )

           #send_whatsapp_message(phone,message)

           return HttpResponseRedirect(reverse('thank-you-rj', args=[tran_detail_obj.id]))

       else:
           write_log("This Transaction ", "Failed")
           return HttpResponseRedirect(reverse('home'))

   except Exception as e:

       write_log("Payment page error", e)  # Use f-string for formatting

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
        if transaction_obj.field1:
            all_title = get_campaign_titles_by_ids(transaction_obj.field1)
        else:
            all_title = ""

        return render(request, 'frontend/invoice_80g.html', {'all_title':all_title,'transaction_obj':transaction_obj})


@csrf_exempt
def payment_success(request):
    razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
    razorpay_subscription_id = request.POST.get('razorpay_subscription_id', '')
    razorpay_signature = request.POST.get('razorpay_signature', '')
    email = request.POST.get('email', '')
    name = request.POST.get('name', '')
    phone_no = request.POST.get('phone_no', '')
    plan_id = request.POST.get('plan_id', '')
    campaign_id = request.POST.get('campaign_id', '')
    params_dict_dd = request.POST.dict()
    subscription_data = razorpay_client.subscription.fetch(razorpay_subscription_id)
    print("This")
    print(subscription_data)
    addons = subscription_data.get('notes', [])
    product_info = addons['title']
    price =addons['amount']

    price = float(price) / 100
    print(addons)
    cow_name = ""
    try:
        cow_name = addons['cow_name']

    except:

        pass
    print(params_dict_dd)
    params_dict = {
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_subscription_id': razorpay_subscription_id,
        'razorpay_signature': razorpay_signature,
    }
    try:
        # Verify the payment signature
        result = razorpay_client.utility.verify_subscription_payment_signature(params_dict)
        password = uuid.uuid4()
        user_obj = create_user(name,email,password,phone_no, 'Devotee','')

        if plan_id:
            plan = SubscriptionPlan.objects.get(plan_id=plan_id)
        else:
            plan = SubscriptionPlan.objects.filter(is_active=True).first()

        campaign = Campaign.objects.get(id=campaign_id)
        # Create the subscription for the user
        subscription = Subscription.objects.create(
            user=user_obj,
            plan=plan,
            campaign=campaign,
            cow_name=cow_name,
            price=price,
            start_date=timezone.now(),
            is_active=True,
            razorpay_subscription_id=razorpay_subscription_id,
            razorpay_payment_id=razorpay_payment_id
        )

        tran_obj = TransactionDetails()
        tran_obj.mihpayid = razorpay_subscription_id
        tran_obj.order_id = razorpay_subscription_id
        tran_obj.campaign_id = campaign_id
        tran_obj.firstname = name
        tran_obj.cow_name = cow_name
        tran_obj.productinfo = product_info
        tran_obj.email = email
        tran_obj.phone = phone_no
        tran_obj.status = 'captured'
        tran_obj.payment_source = 'Online'
        tran_obj.mode = 'Online'
        tran_obj.amount = price
        tran_obj.save()

        if not request.user.is_authenticated:
            login(request, user_obj)

        receipt_url = settings.BASE_URL + "/receipt/" + str(tran_obj.id)
        send_donation_thank_you_email(name, email, float(price), receipt_url)
        write_log("Message send for ", email)
        # login(request, user_obj)

        invoice_link = settings.BASE_URL + str(tran_obj.id)
        message = (
            f"🕉️ *Hingonia* 🕉️\n\n"
            f"Dear {name},\n\n"
            "🙏 *Thank you for your generous donation!* 🙏\n\n"
            "We are truly grateful for your support towards our mission. "
            f"Your contribution of ₹{price} will go a long way in supporting our cause and making a positive impact.\n\n"
            "You can download your invoice from the following link:\n"
            f"{invoice_link}\n\n"  # Add the invoice link dynamically
            "If you have any queries or would like to stay updated on our activities, "
            "feel free to contact us at +91 9112524911 or visit our website.\n\n"
            "May Lord Shiva's blessings be with you always.\n\n"
            "*Om Namah Shivaya* 🙏\n\n"
            "Hingonia"
        )

        #send_whatsapp_message(phone_no, message)

        return HttpResponseRedirect(reverse('thank-you-rj', args=[tran_obj.id]))

        # Payment is successful
    except razorpay.errors.SignatureVerificationError:
        # Payment failed
        messages.error(request, 'Payment failed.')

        return HttpResponseRedirect(reverse('Home'))


def get_campaign_titles_by_ids(id_string):
    # Convert the comma-separated string of IDs into a list of integers
    ids = [int(id) for id in id_string.split(',')]

    # Query campaigns by the list of IDs
    campaigns = Campaign.objects.filter(id__in=ids)

    # Extract the 'title' of each campaign and join them into a comma-separated string
    campaign_titles = campaigns.values_list('title', flat=True)

    return ','.join(campaign_titles)

class DownloadReceiptView(View):
    def get(self, request,id):
        # Get the HTML template
        transaction_obj = TransactionDetails.objects.get(id=id)
        if transaction_obj.field1:
            all_title = get_campaign_titles_by_ids(transaction_obj.field1)
        else:
            all_title = ""

        return render(request, 'frontend/receipt.html', {'all_title':all_title,'transaction_obj':transaction_obj})


class VerifyOTPView(View):
    template_name = 'frontend/verify_otp.html'
    form_class = VerifyOTPForm

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        form = self.form_class(initial={'user_id': user_id})  # Pass user_id to the form

        return render(request, self.template_name, {'form': form,'user_id':user_id})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            new_password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            user_id = form.cleaned_data['user_id']

            user = User.objects.get(id=user_id)
            if user:
                otp_obj = OTP.objects.filter(user=user, otp=otp, expiration__gte=timezone.now()).first()
                if otp_obj:
                    if new_password == confirm_password:
                        if otp_obj.expiration >= timezone.now():
                            user.set_password(new_password)
                            user.save()
                            otp_obj.delete()
                            messages.success(request, 'Password reset successful. You can now login with your new password.')
                            return redirect('user-login')
                        else:
                            messages.error(request, 'OTP has expired. Please request a new OTP.')
                    else:
                        messages.error(request, 'New password and confirm password do not match.')
                else:
                    messages.error(request, 'Invalid OTP or OTP has expired. Please request a new OTP.')
            else:
                messages.error(request, 'No user found with this email address.')
        return render(request, self.template_name, {'form': form})


class ForgotPasswordView(View):
    def get(self, request, token=''):
        return render(request, 'frontend/forgot_password.html')

    def post(self, request):
        # Retrieve the email from the POST data
        email = request.POST.get("email")

        try:
            # Try to get the user with the provided email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')

            # If the user does not exist, render the form with an error message
            return render(request, 'frontend/forgot_password.html', {'error': 'User with this email does not exist.'})

        # Generate a password reset token for the user
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        # Generate the password reset link
        reset_link = f"{settings.BASE_URL}/reset-password/{user.pk}/{token}/"

        # Prepare the email context and send the email
        context = {
            'username': user.first_name or user.username,  # Use first name or fallback to username
            'reset_link': reset_link,
        }
        subject = "Password Reset Request"
        send_email(request,email,'email/password_reset_email.html',context, subject)
        messages.success(request, 'Password reset link has been sent to your email.')
        # Render the form with a success message
        return render(request, 'frontend/forgot_password.html', {'message': 'Password reset link has been sent to your email.'})


class ResetPasswordView(View):
    template_name = 'frontend/reset-forgot-password.html'

    def get(self, request, uidb64, token):
        # Render the form for entering a new password
        context = {'uidb64': uidb64, 'token': token}
        return render(request, self.template_name, context)

    def post(self, request, uidb64, token):
        # Decode the user ID from the uidb64 parameter
        try:
            uid = uidb64
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return render(request, self.template_name, {'error': "Invalid link or expired."})

        # Verify the token
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return render(request, self.template_name, {'error': "Invalid token."})

        # Get the new password from the form
        new_password = request.POST.get('new_password')
        if not new_password:
            return render(request, self.template_name, {'error': "New password is required."})

        # Set the new password and save the user
        user.set_password(new_password)
        user.save()

        messages.success(request, "Password has been successfully reset.")
        return redirect('thank-you-reset')  # Redirect to the login page or another desired page


class ThankYouResetView(View):
    template_name = 'frontend/thank_you_reset.html'

    def get(self, request):
        # Render the form for entering a new password
        context = {'FRONT_URL': reverse('user-login')}
        return render(request, self.template_name, context)


def reset_password(request, token):
    # Handle password reset logic here
    pass

def subscribe_page(request):
    context = {
        'razorpay_key_id': settings.RAZOR_PAY_ID,
        'amount': 1000,  # Amount in paise (₹500)
    }
    return render(request, 'frontend/subscribe.html',context)

def create_subscription(request):
    if request.method == 'POST':
        if request.POST.get('amount'):
            print("Amount")
            print(request.POST.get('amount'))
            amount = float(request.POST.get('amount')) * 100  # Convert amount to paise
        else:
            amount = float(request.POST.get('custom_number')) * 100  # Convert amount to paise

        name = request.POST['name']
        cow_name = request.POST['cow_name']
        campaign_id = request.POST['campaign_id']
        email = request.POST['email']
        phone_no = request.POST['phone_no']
        preferred_date = request.POST['preferred_date']
        title = request.POST['title']

        # Convert the preferred date to a timestamp
        preferred_date_obj = datetime.strptime(preferred_date, '%Y-%m-%d')
        current_date = datetime.now()
        campaign_obj = Campaign.objects.get(id=campaign_id)
        # If the preferred date is in the past, schedule for the next month
        if preferred_date_obj < current_date:
            preferred_date_obj = preferred_date_obj.replace(year=current_date.year,
                                                            month=current_date.month) + timedelta(days=30)

        # Convert preferred date to a UNIX timestamp
        start_at = int(preferred_date_obj.timestamp())
        if not request.POST['plan_id']:
            plan_id = 'plan_P7fZefpGT4WdAp'
        else:
            plan_id = request.POST['plan_id']
        if not cow_name:
            cow_name = ""
        if plan_id:
            print("Plan id")
            print(plan_id)
            plan = SubscriptionPlan.objects.filter(plan_id=plan_id).first()
            print("PT price")
            print(plan.price)
            subscription_data = {
                "plan_id": plan_id,
                "customer_notify": 1,
                "total_count": 12,  # Optional, for a one-year subscription
                "quantity": 1,
                "start_at": start_at,  # Set the start date for the subscription
                "addons": [{
                    "item": {
                        "name": "Monthly Donation",
                        "amount": amount,
                        "currency": "INR"
                    }
                }],
                "notes": {
                    "amount": amount,
                    "name": name,
                    "title":title,
                    "cow_name":cow_name,
                    "for": campaign_obj.title,
                    "email": email,
                    "phone_no": phone_no,
                    "campaign_id": campaign_id
                }
            }
            # amount = amount - float(plan.price)
        else:
            plan = SubscriptionPlan.objects.filter(is_active=True).first()
            # amount = amount - float(plan.price)*99
            plan_id = plan.plan_id
            print("HERE it came")
            print(plan_id)
            subscription_data = {
                "plan_id": plan_id,
                "customer_notify": 1,
                "total_count": 12,  # Optional, for a one-year subscription
                "start_at": start_at,  # Set the start date for the subscription

                "quantity": 1,
                "addons": [{
                    "item": {
                        "name": "Monthly Donation",
                        "amount": amount,
                        "currency": "INR"
                    }
                }],
                "notes": {
                    "amount": amount,
                    "for": campaign_obj.title,
                    "name": name,
                    "cow_name":cow_name,
                    "title": title,
                    "email": email,
                    "phone_no": phone_no,
                    "campaign_id":campaign_id
                }
            }

        print(subscription_data)

        subscription = razorpay_client.subscription.create(data=subscription_data)
        return JsonResponse(subscription)

