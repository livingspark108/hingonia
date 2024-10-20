"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
# Django imports
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView
from django.urls import path, include, re_path
from django.conf import settings



urlpatterns = [
    #fontend urls
    path('', include('frontend.urls')),
    # auth urls
    path('admin/', include('apps.authentication.urls')),
    # admin urls
    path('admin/', include('apps.administrator.urls')),
    path('front_app/', include('apps.front_app.urls')),
    # enable the admin interface
    url(r'^administration', admin.site.urls),
    # auth urls
    # path('password_reset/', PasswordResetView.as_view(
    #     html_email_template_name='registration/forgot_password.html'
    # ), name='password_reset'),
    path('', include('django.contrib.auth.urls')),
    # Ckeditor urls
    path('ckeditor/', include('ckeditor_uploader.urls')),
    #logs
    path('logs/', include('logs.urls')),

    #cms urls
    path('cms/', include('apps.cms.urls')),
    path('promoter/', include('apps.promoter.urls')),
    #user urls
    path('user/', include('apps.user.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
