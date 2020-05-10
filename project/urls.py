"""smarttrucking URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from .views import LoginView, LogoutView, ChangePasswordView, load_state
from django.conf import settings
from app.views import *
from django.conf.urls.static import static

from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # API
    # Auth Urls
    path('admin/', LoginView.as_view(), name="sys_login"),
    path('logout/', LogoutView.as_view(), name="sys_logout"),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
    path('', include('django.contrib.auth.urls')),

    # Admin Urls
    path('administration/', admin.site.urls),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('load_state/',load_state),
    path('users/', ListUsersView.as_view(), name='list_users'),
    path('users/add/', CreateUserView.as_view(), name='add_user'),
    path('users/<int:pk>/', DetailUserView.as_view(), name='user_detail'),
    path('users/<int:pk>/edit/', UpdateUserView.as_view(), name='update_user'),
    path('users/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),
    path('<int:pk>/<str:status>/change_user_status/', change_user_status, name='change_user_status'),
    path('admin/<int:pk>/edit/', staff_member_required(UpdateUserView.as_view(), login_url='change_user_status'),
         name='update_admin'),

    path('master/', include('settings.urls'), name='settings'),

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)