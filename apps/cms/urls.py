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

from apps.cms.views import CreatePageView, ListPagesView, ListPagesViewJson, UpdatePageView, DeletePageView

urlpatterns = [
    path('page/add', CreatePageView.as_view(), name='page-add'),
    path('page/', ListPagesView.as_view(), name='page-list'),
    path('page/list/ajax', ListPagesViewJson.as_view(), name='page-list-ajax'),
    path('page/edit/<int:pk>', UpdatePageView.as_view(), name='page-edit'),
    path('page/delete/<int:pk>', DeletePageView.as_view(), name='page-delete'),
]

