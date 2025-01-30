# Python imports
from os.path import abspath, basename, dirname, join, normpath
import sys
from django.contrib import messages
import os
# ##### PATH CONFIGURATION ################################

# fetch Django's project directory
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# fetch the project_root
PROJECT_ROOT = dirname(DJANGO_ROOT)

# the name of the whole site
SITE_NAME = basename(DJANGO_ROOT)

# collect static files here
STATIC_ROOT = join(PROJECT_ROOT, 'run', 'static')

# collect media files here
MEDIA_ROOT = join(PROJECT_ROOT, 'run', 'media')

# look for static assets here
STATICFILES_DIRS = [
    join(PROJECT_ROOT, 'static'),
]

# look for templates here
# This is an internal setting, used in the TEMPLATES directive
PROJECT_TEMPLATES = [
    join(PROJECT_ROOT, 'templates'),
]

# add apps/ to the Python path
sys.path.append(normpath(join(PROJECT_ROOT, 'apps')))

LOGIN_URL = 'auth-login'
LOGOUT_REDIRECT_URL = 'auth-login'
# ##### APPLICATION CONFIGURATION #########################

# these are the apps
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'theme',
    'rest_framework',
    'apps.authentication',
    'apps.administrator',
    'apps.cms',
    'apps.user',
    'apps.promoter',
    'apps.front_app',
    'logs',
    'frontend',
    'widget_tweaks',
    'payu',
    'ckeditor',
    'ckeditor_uploader',
    #keep below app in last only
    'django_cleanup',
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# template stuff
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': PROJECT_TEMPLATES,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'django_settings_export.settings_export',
                'application.context_processor.device_type',
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = [
    'application.custom_classes.EmailOrUsernameBackend',  # Custom email or username backend
    'django.contrib.auth.backends.ModelBackend',      # Default backend
]


# Internationalization
USE_I18N = False

# ##### SECURITY CONFIGURATION ############################

# We store the secret key here
# The required SECRET_KEY is fetched at the end of this file
SECRET_FILE = normpath(join(PROJECT_ROOT, 'run', 'SECRET.key'))

# these persons receive error notification
ADMINS = (
    ('your name', 'your_name@example.com'),
)
MANAGERS = ADMINS
ADMIN_EMAIL = 'livingsparkglobal@gmail.com'
# ##### DJANGO RUNNING CONFIGURATION ######################

# the default WSGI application
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

# the root URL configuration
ROOT_URLCONF = '%s.urls' % SITE_NAME

# the URL for static files
STATIC_URL = '/static/'

# the URL for media files
MEDIA_URL = '/media/'

# ##### DEBUG CONFIGURATION ###############################
DEBUG = False

#### Project name confix
APP_NAME = 'Hingonia';

SETTINGS_EXPORT = [
    'APP_NAME',
]
SETTINGS_EXPORT_VARIABLE_NAME = 'configs'

AUTH_USER_MODEL = 'user.User'

MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

CKEDITOR_UPLOAD_PATH = "content_files/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'height': 500,
        'width': 742,
        'toolbar_Custom': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker', 'Undo', 'Redo'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'], ['Source'],
        ],
    },
    'special': {
        'toolbar': 'Special',
        'toolbar_Special': [
            ['Bold'], ['CodeSnippet'],
        ],
        'extraPlugins': 'codesnippet',
    }
}

# Chat settings
CHAT_WS_SERVER_HOST = '206.81.12.161'
CHAT_WS_SERVER_PORT = 5002
CHAT_WS_SERVER_PROTOCOL = 'ws'

# finally grab the SECRET KEY
try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        from django.utils.crypto import get_random_string

        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!$%&()=+-_'
        SECRET_KEY = get_random_string(50, chars)
        with open(SECRET_FILE, 'w') as f:
            f.write(SECRET_KEY)
    except IOError:
        raise Exception('Could not open %s for writing!' % SECRET_FILE)

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "BNuZS1QnexQty7SI2JH5JBF57elpUj2ujXX292ur_lHxyHhqvJW_DbVMzaaLTCDxuLX0jwqBi7OT1gPz1iKiels",
    "VAPID_PRIVATE_KEY": "kdtfl4mj-nVi_trBGlH67XgUFvKrY0EhDKfIdwL8iI4",
    "VAPID_ADMIN_EMAIL": "nairsukumarandeepak@gmail.com"
}
USE_TZ = False
TIME_ZONE = 'Asia/Kolkata'

# added for user profile image resize/compress
DJANGORESIZED_DEFAULT_SIZE = [300, 300]
DJANGORESIZED_DEFAULT_QUALITY = 60
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

#Free plan config
CLASS_ALLOWED = 1
SUBJECT_ALLOWED = 1
VIDEO_ALLOWED = 5

CSRF_COOKIE_AGE = 36000  # 1 hour in seconds


# Stripe configuration
STRIPE_LIVE_MODE = False  # Change to True in production
STRIPE_LIVE_PUBLIC_KEY = 'pk_test_TwkLoEwoTo9rrRq84uY1zezg00Jlk3x1oK'
STRIPE_LIVE_SECRET_KEY = 'sk_test_6p80GWQU7si4C2foYzEAzQSP00o0E31HXF'
STRIPE_TEST_PUBLIC_KEY = 'pk_test_TwkLoEwoTo9rrRq84uY1zezg00Jlk3x1oK'
STRIPE_TEST_SECRET_KEY = 'sk_test_6p80GWQU7si4C2foYzEAzQSP00o0E31HXF'

DJSTRIPE_WEBHOOK_SECRET = "whsec_11ov9HJBLwcI7AmXPWU5DcjljMgE6Df0"  # Get it from the section in the Stripe dashboard where you added the webhook endpoint



#Email Server
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'hcrc.skbt@gmail.com'
EMAIL_HOST_PASSWORD = 'gbdy idof uvxj ekjm'
EMAIL_USE_TLS = True
admin_email = 'hcrc.skbt@gmail.com'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'hcrc.skbt@gmail.com'


FILE_UPLOAD_PERMISSIONS = 0o644

PAYU_CONFIG = {

    "merchant_key":"tM5HOf",
    "merchant_salt":"WMMC7MXGhU9p1cbn8PGgB5msXUA8I7E2",
    "mode": "Live",
    "RESPONSE_URL_SUCCESS" : "https://thepuredevotion.in/payment_response_handler/",
    "RESPONSE_URL_FAILURE" : "https://thepuredevotion.in/payment_failed_handler/"
   }
# Change the PAYU_MODE to 'LIVE' for production.
PAYU_MODE = "TEST"

CSRF_TRUSTED_ORIGINS = ['https://secure.payu.in']

GOOGLE_ANALYTICS = {
    'google_analytics_id': 'UA-165462357-1',
}

# RAZOR_PAY_ID = "rzp_test_AhOuknmPQlm0es"
# RAZOR_PAY_SECRET = "94cAr5eXW4pJ9f0ZEjkmo2gG"

RAZOR_PAY_ID = "rzp_live_72nKopHGn9HWKB"
RAZOR_PAY_SECRET = "Sw8goe5ZkOeFcElzJn96MB8A"

#Live
SMS_AUTH_KEY = '4b358371ef203b2a4c3c7c0e1f56197'
SMS_URL = "http://msg.msgclub.net/rest/services/sendSMS/sendGroupSms"
SENDER_ID = "LVGMNU"

AUTH_USER_MODEL = 'user.User'


# Define BASE_DIR
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Logging configuration


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'daily_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/errors.log'),
            'when': 'midnight',  # Rotate at midnight
            'interval': 1,       # Every day
            'backupCount': 300,  # Keep 300 old log files
            'formatter': 'error',
        },
        'custom_file': {  # New handler for logging custom events
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/custom.log'),
            'when': 'midnight',  # Rotate at midnight
            'interval': 1,       # Every day
            'backupCount': 30,   # Keep 30 old log files
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'error': {
            'format': '{levelname} {asctime} {module} {filename}:{lineno} - {message}\n\n--------{asctime}----------\n\n',
            'style': '{',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['daily_file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'custom_logger': {  # New custom logger for general logs
            'handlers': ['custom_file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}