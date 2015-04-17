INSTALLED_APPS = (
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'social.apps.django_app.default',
    'sekizai',
    'bootstrap3',
    'django_countries',
    'simple_history',
    'venues',
    "widget_tweaks", # for form add class
    'django_assets',
    'autoslug',
    'google_analytics'
)

GOOGLE_ANALYTICS_MODEL = True
GOOGLE_ANALYTICS_TRACK_PAGE_LOAD_TIME = True