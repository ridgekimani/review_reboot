import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


try:
    credentials_path = ""
    credentials_path = os.path.join(BASE_DIR, "credentials.json")
    credentials = json.load(open(credentials_path))
except IOError as e:
    print("check existance of %s" % credentials_path)
    raise e

SITE_ID = 1
SECRET_KEY = credentials['SECRET_KEY']
ALLOWED_HOSTS = credentials['ALLOWED_HOSTS']
DEBUG = int(credentials['DEBUG']) == 1
TEMPLATE_DEBUG = DEBUG

from restaurant.settings.apps import *
from restaurant.settings.database import *
from restaurant.settings.dirs import *
from restaurant.settings.middleware import *
from restaurant.settings.social import *

ROOT_URLCONF = 'restaurant.urls'

WSGI_APPLICATION = 'restaurant.wsgi.application'

LOGIN_URL = '/login/facebook/'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

