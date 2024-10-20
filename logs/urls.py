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
from logs.views import *

urlpatterns = [
    path('view-logs/', ErrorLogViewerView.as_view(), name='log_viewer'),
    path('view-logs/<str:date>/', ErrorLogViewerSingleView.as_view(), name='log_viewer_s'),
    path('view-logger/', CustomLogViewerView.as_view(), name='custom_log_viewer'),
    path('view-logger/<str:date>/', CustomLogViewerSingleView.as_view(), name='custom_log_viewer_single'),
]

