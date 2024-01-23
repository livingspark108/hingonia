# Python imports
from os.path import abspath, basename, dirname, join, normpath
import sys
from django.contrib import messages

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
    'apps.authentication',
    'apps.administrator',
    'apps.cms',
    'apps.user',
    'apps.front_app',
    'frontend',
    'widget_tweaks',
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
            ],
        },
    },
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
APP_NAME = 'Mata ji Admin';

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
USE_TZ = True
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



# Stripe configuration
STRIPE_LIVE_MODE = False  # Change to True in production
STRIPE_LIVE_PUBLIC_KEY = 'pk_test_TwkLoEwoTo9rrRq84uY1zezg00Jlk3x1oK'
STRIPE_LIVE_SECRET_KEY = 'sk_test_6p80GWQU7si4C2foYzEAzQSP00o0E31HXF'
STRIPE_TEST_PUBLIC_KEY = 'pk_test_TwkLoEwoTo9rrRq84uY1zezg00Jlk3x1oK'
STRIPE_TEST_SECRET_KEY = 'sk_test_6p80GWQU7si4C2foYzEAzQSP00o0E31HXF'

DJSTRIPE_WEBHOOK_SECRET = "whsec_11ov9HJBLwcI7AmXPWU5DcjljMgE6Df0"  # Get it from the section in the Stripe dashboard where you added the webhook endpoint


#Email Server
EMAIL_HOST = 'imap.secureserver.net'
EMAIL_PORT = 993
EMAIL_HOST_USER = 'bhavanshu@livingspark.in'
EMAIL_HOST_PASSWORD = '08019@Hkc'
EMAIL_USE_TLS = True


FILE_UPLOAD_PERMISSIONS = 0o644


GOOGLE_ANALYTICS = {
    'google_analytics_id': 'UA-165462357-1',
}
