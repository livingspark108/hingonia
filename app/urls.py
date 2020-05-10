from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^login/', CustomAuthToken.as_view()),
    url(r'^forgot_pass/', ForgotPassAPIView.as_view()),
    url(r'^register/', UserCreateAPIView.as_view()),
]
