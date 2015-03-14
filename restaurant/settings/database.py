import sys
from restaurant.settings import credentials

POSTGIS_VERSION = (2, 1, 2)

if sys.argv[1] == "test":
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.spatialite',
            'NAME': 'db/test.sqlite',
        }
    }
else:
    DATABASES = {
        'default': credentials['database']
    }
