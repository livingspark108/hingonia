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
    path('our-mothers', FrontendOurMotherView.as_view(), name='our-mothers'),
    path('campaign', FrontendCampaignView.as_view(), name='campaign'),
    path('distribution', FrontendDistributionView.as_view(), name='distribution'),
    path('distribution/<str:pk>', FrontendDistributionDetailView.as_view(), name='distribution_detail'),
    path('my-donation', FrontendDonationView.as_view(), name='my-donation'),
    path('profile', FrontendProfileView.as_view(), name='profile'),
    path('user-login', FrontendLoginView.as_view(), name='user-login'),
    path('user-logout/', UserLogoutView.as_view(), name="user-logout"),
    path('save-abandon/', AbandonView.as_view(), name="save-abandon"),

    path('privacy-policy', FrontendPrivacyPolicyView.as_view(), name='privacy-policy'),
    path('term-and-condition', FrontendTermConditionView.as_view(), name='term-and-condition'),
    path('refund-policy', FrontendRefundPolicyView.as_view(), name='refund-policy'),
    path('pay', FrontendPayView.as_view(), name='pay'),
    path('pay_now', FrontendPayView.as_view(), name='pay'),
    path('thank-you', FrontendThankYouView.as_view(), name='thank-you'),
    path('payment_response_handler/', PayuSuccessAPiView.as_view(), name='payu-success-api'),
    path('payment_response_handler/', PayuFailureAPiView.as_view(), name='payu-failed-api'),
    path('set_password/', set_password, name='set_password'),
    path('download-80g/<str:id>', Download80gView.as_view(), name='download-80g'),
    path('request-80g', Request80GView.as_view(), name="request-80g"),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', reset_password, name='reset_password'),
    path('ongoing-devotion/', OngoingDevotionView.as_view(), name='ongoing-devotion'),

]

