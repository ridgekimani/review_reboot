from restaurant.settings import credentials

__author__ = 'm'

POSTGIS_VERSION = (2, 1, 2)


DATABASES = {
    'default': credentials['database']
}
