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

from apps.front_app.views import *

urlpatterns = [
    #"""Campaign page"""
    path('campaign/add', CreateCampaignView.as_view(), name='campaign-add'),
    path('campaign/', ListCampaignView.as_view(), name='campaign-list'),
    path('campaign/list/ajax', ListCampaignViewJson.as_view(), name='campaign-list-ajax'),
    path('campaign/edit/<str:pk>', UpdateCampaignView.as_view(), name='campaign-edit'),
    path('campaign/delete/<str:pk>', DeleteCampaignView.as_view(), name='campaign-delete'),

    #"""Mother page"""
    path('mother/add', CreateMotherView.as_view(), name='mother-add'),
    path('mother/', ListMotherView.as_view(), name='mother-list'),
    path('mother/list/ajax', ListMotherViewJson.as_view(), name='mother-list-ajax'),
    path('mother/edit/<str:pk>', UpdateMotherView.as_view(), name='mother-edit'),
    path('mother/delete/<str:pk>', DeleteMotherView.as_view(), name='mother-delete'),

    #"""Our Team"""
    path('ourteam/add', CreateOurTeamView.as_view(), name='ourteam-add'),
    path('ourteam/', ListOurTeamView.as_view(), name='ourteam-list'),
    path('ourteam/list/ajax', ListOurTeamViewJson.as_view(), name='ourteam-list-ajax'),
    path('ourteam/edit/<str:pk>', UpdateOurTeamView.as_view(), name='ourteam-edit'),
    path('ourteam/delete/<str:pk>', DeleteOurTeamView.as_view(), name='ourteam-delete'),

    #Distribution

    path('distribution/add', CreateDistributionView.as_view(), name='distribution-add'),
    path('distribution/', ListDistributionView.as_view(), name='distribution-list'),
    path('distribution/list/ajax', ListDistributionViewJson.as_view(), name='distribution-list-ajax'),
    path('distribution/edit/<str:pk>', UpdateDistributionView.as_view(), name='distribution-edit'),
    path('distribution/delete/<str:pk>', DeleteDistributionView.as_view(), name='distribution-delete'),


    #""" Update About us """

    path('update-about-us/', UpdateAboutUsView.as_view(), name='update-about-us'),

    path('donation-list/', ListDonationView.as_view(), name='donation_list'),
    path('donation-list/ajax', ListDonationViewJson.as_view(), name='donation-list-ajax'),

]

