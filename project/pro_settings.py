from .settings import *


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'mls_db',
        'USER': 'mls_user',
        'PASSWORD': '123456',
        'HOST': 'localhost'
    }
}
