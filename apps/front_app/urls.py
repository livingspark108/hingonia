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
    path('campaign/clone/<str:pk>', CloneCampaignView.as_view(), name='campaign-clone'),

    path('testimonial/add', CreateTestimonialView.as_view(), name='testimonial-add'),
    path('testimonial/', ListTestimonialView.as_view(), name='testimonial-list'),
    path('testimonial/list/ajax', ListTestimonialViewJson.as_view(), name='testimonial-list-ajax'),
    path('testimonial/edit/<str:pk>', UpdateTestimonialView.as_view(), name='testimonial-edit'),
    path('testimonial/delete/<str:pk>', DeleteTestimonialView.as_view(), name='testimonial-delete'),
    path('testimonial/clone/<str:pk>', CloneTestimonialView.as_view(), name='testimonial-clone'),


    #***** Campaign Product ******
    path('campaign-product/add', CreateCampaignProductView.as_view(), name='campaign-product-add'),
    path('campaign-product/', ListCampaignProductView.as_view(), name='campaign-product-list'),
    path('campaign-product/list/ajax', ListCampaignProductViewJson.as_view(), name='campaign-product-list-ajax'),
    path('campaign-product/edit/<str:pk>', UpdateCampaignProductView.as_view(), name='campaign-product-edit'),
    path('campaign-product/delete/<str:pk>', DeleteCampaignProductView.as_view(), name='campaign-product-delete'),

    #"""Product page"""
    path('product/add', CreateProductView.as_view(), name='product-add'),
    path('product/', ListProductView.as_view(), name='product-list'),
    path('product/list/ajax', ListProductViewJson.as_view(), name='product-list-ajax'),
    path('product/edit/<str:pk>', UpdateProductView.as_view(), name='product-edit'),
    path('product/delete/<str:pk>', DeleteProductView.as_view(), name='product-delete'),

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
    path('setting/', UpdateSettingView.as_view(), name='setting'),
    path('whatsapp/', WhatsAppDashboardView.as_view(), name='whatsapp'),

    path('donation-list/', ListDonationView.as_view(), name='donation_list'),
    path('donation-list/ajax', ListDonationViewJson.as_view(), name='donation-list-ajax'),

    path('abandon-list/', ListAbandonView.as_view(), name='abandon-list'),
    path('abandon-list/ajax', ListAbandonViewJson.as_view(), name='abandon-list-ajax'),

    path('80g-request-list/', List80GRequestView.as_view(), name='80g-request-list'),
    path('80g-request-approve/<str:id>', Apporve80GView.as_view(), name='80g-request-approve'),
    path('80g-request-list/ajax', List80GRequestViewJson.as_view(), name='80g-request-list-ajax'),

    # Monthly Subscriber

    path('monthly-subscriber/', ListAbandonView.as_view(), name='monthly-subscriber'),
    path('monthly-subscriber/ajax', ListAbandonViewJson.as_view(), name='monthly-subscriber-ajax'),

    path('upload/', file_upload_view, name='file_upload'),
    path('files/', file_list_view, name='file_list'),
    path('delete/', file_delete_view, name='file_delete'),

    path('home-page-setting/', HomePageSettingView.as_view(), name='home-page-setting'),

    #"""Mother page"""
    path('order/', ListOrderView.as_view(), name='order-list'),
    path('order/list/ajax', ListOrderViewJson.as_view(), name='order-list-ajax'),
    path('order/edit/<str:pk>', UpdateOrderView.as_view(), name='order-edit'),
    path('order/delete/<str:pk>', DeleteOrderView.as_view(), name='order-delete'),
]

