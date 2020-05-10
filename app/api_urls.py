from django.conf.urls import url
from django.urls import include

from .api import *

urlpatterns = [
    url('auth/login/', LoginAuthAPIView.as_view()),
    url('auth/register/', UserRegisterAPIView.as_view()),
    url('auth/list/', ListUserAPIView.as_view()),
    url('auth/get_user_data/', ListSingleUserDataAPIView.as_view()),
    url('auth/add_shipping/', CreateUserShippingAPIView.as_view()),
    url('auth/update_shipping/', UpdateUserShippingAPIView.as_view()),
    url('auth/delete_shipping/', DeleteUserShippingAPIView.as_view()),
    url('auth/update_user_address/', UpdateUserAddressAPIView.as_view()),
    url('auth/change_password/', UserChangePasswordAPIView.as_view()),
    url('auth/update_profile/', UpdateUserAPIView.as_view()),
    url('auth/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    url('auth/country_list/', ListCountryListAPIView.as_view()),
    url('auth/state_list/', ListStateListAPIView.as_view()),
]
