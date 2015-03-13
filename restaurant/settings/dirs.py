import os
from restaurant.settings import BASE_DIR

__author__ = 'm'

STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'restaurant/static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
#STATICFILES_DIRS = ( os.path.join('static'),)
#MEDIA_ROOT = '/home/django/django_project/static'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "restaurant/templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    "account.context_processors.account",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "sekizai.context_processors.sekizai",
    # "pinax_theme_bootstrap.context_processors.theme",
)