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
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('add', CreatePromoterView.as_view(), name='promoter-add'),
    path('', ListPromoterView.as_view(), name='promoter-list'),
    path('list/ajax', ListPromoterViewJson.as_view(), name='promoter-list-ajax'),
    path('edit/<str:pk>', UpdatePromoterView.as_view(), name='promoter-edit'),
    path('delete/<str:pk>', DeletePromoterView.as_view(), name='promoter-delete'),
    path('view-campaign/<str:id>', ListCompaignPromoView.as_view(), name='view-campaign'),

]


