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
from frontend.views import *
urlpatterns = [
    path('', FrontendHomeView.as_view(), name='home'),
    path('about-us', FrontendAboutUsView.as_view(), name='about-us'),
    path('our-mothers', FrontendOurMotherView.as_view(), name='our-mothers'),
    path('campaign', FrontendCampaignView.as_view(), name='campaign'),
    path('distribution', FrontendDistributionView.as_view(), name='distribution'),
    path('privacy-policy', FrontendPrivacyPolicyView.as_view(), name='privacy-policy'),
    path('term-and-condition', FrontendTermConditionView.as_view(), name='term-and-condition'),
    path('refund-policy', FrontendRefundPolicyView.as_view(), name='refund-policy'),

]

