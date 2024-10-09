"""application admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
from frontend import views
from frontend.views import *

urlpatterns = [

    path('', FrontendHomeView.as_view(), name='home'),
    path('about-us', FrontendAboutUsView.as_view(), name='about-us'),
    path('trustees', FrontendTrusteeView.as_view(), name='trustee'),
    path('our-mothers', FrontendOurMotherView.as_view(), name='our-mothers'),
    path('campaign', FrontendCampaignView.as_view(), name='campaign'),
    path('distribution', FrontendDistributionView.as_view(), name='distribution'),
    path('distribution/<str:pk>', FrontendDistributionDetailView.as_view(), name='distribution_detail'),
    path('my-donation', FrontendDonationView.as_view(), name='my-donation'),
    path('profile', FrontendProfileView.as_view(), name='profile'),
    path('user-login', FrontendLoginView.as_view(), name='user-login'),
    path('user-logout/', UserLogoutView.as_view(), name="user-logout"),
    path('save-abandon/', AbandonView.as_view(), name="save-abandon"),
    path('get_campaign/<str:pk>', GetCampaignView.as_view(), name='get_campaign'),
    path('csr', CsrView.as_view(), name='csr'),
    path('adopted-cow', AdoptedCowView.as_view(), name='adopted-cow'),
    path('waiting-cow', WaitingCowView.as_view(), name='waiting-cow'),
    path('seva', SevaView.as_view(), name='seva'),
    path('our-supporters', OurSupportersView.as_view(), name='our-supporters'),
    path('gallery', FrontendDistributionView.as_view(), name='gallery'),
    path('gallery/<str:pk>', FrontendDistributionDetailView.as_view(), name='distribution_detail'),
    path('product', ProductView.as_view(), name='product'),

    path('privacy-policy', FrontendPrivacyPolicyView.as_view(), name='privacy-policy'),
    path('term-and-condition', FrontendTermConditionView.as_view(), name='term-and-condition'),
    path('refund-policy', FrontendRefundPolicyView.as_view(), name='refund-policy'),
    path('pay', FrontendPayView.as_view(), name='pay'),
    path('razor-pay', FrontendRazorPayView.as_view(), name='razor-pay'),
    path('success-pay', payment_success_view, name='razor-pay-success'),
    path('pay_now', FrontendPayView.as_view(), name='pay'),
    path('thank-you-hf', FrontendThankYouView.as_view(), name='thank-you'),
    path('thank-you', FrontendRazorThankYouView.as_view(), name='thank-you-rj'),
    path('payment_response_handler/', PayuSuccessAPIView.as_view(), name='payu-success-api'),
    path('payment_failed_handler/', PayuFailureAPiView.as_view(), name='payu-failed-api'),
    path('set_password/', set_password, name='set_password'),
    path('download-80g/<str:id>', Download80gView.as_view(), name='download-80g'),
    path('request-80g', Request80GView.as_view(), name="request-80g"),
    path('send-csr', SendCSRView.as_view(), name="send-csr"),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('verify-otp/<str:user_id>', VerifyOTPView.as_view(), name='verify_otp'),
    path('reset-password/<str:token>/', reset_password, name='reset_password'),

    path('ongoing-devotion/<str:id>', OngoingDevotionView.as_view(), name='ongoing-devotion'),
    path('ongoing-devotion/<str:id>/<str:promo_no>', OngoingDevotionPromoView.as_view(), name='ongoing-devotion-promo'),
    path('pay-razor-pay/', initiate_payment, name='pay-razor-pay'),
    path('handle-payment-webhook/', handle_payment_webhook, name='handle-payment-webhook'),

    path('subscribe', subscribe_page, name='subscribe_page'),
    path('create_subscription/', create_subscription, name='create_subscription'),
    path('get_campaign_product/',  GetCampaignProductView.as_view(), name='get_campaign_product'),
]

