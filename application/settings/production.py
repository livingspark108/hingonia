# Python imports
import os
from os.path import join

# project imports
from .common import *

# uncomment the following line to include i18n
# from .i18n import *


# ##### DEBUG CONFIGURATION ###############################
DEBUG = True


# allow all hosts during development
ALLOWED_HOSTS = ['*']
BASE_URL = "http://167.71.230.81:8014/"
# adjust the minimal login
# LOGIN_URL = 'core_login'
# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = 'core_login'

PAYU_CONFIG = {

    "merchant_key":"tM5HOf",
    "merchant_salt":"WMMC7MXGhU9p1cbn8PGgB5msXUA8I7E2",
    "mode": "Live",
    "RESPONSE_URL_SUCCESS" : "http://127.0.0.1:8010/payment_response_handler/",
    "RESPONSE_URL_FAILURE" : "http://127.0.0.1:8010/payment_response_handler/"
   }

##### DATABASE CONFIGURATION ############################
DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'hingonia',

        'USER': 'postgres',

        'PASSWORD': 'postgres@123#',

        'HOST': 'localhost',

        'PORT': '5432',

    }

}

# ##### APPLICATION CONFIGURATION #########################
INSTALLED_APPS = DEFAULT_APPS

