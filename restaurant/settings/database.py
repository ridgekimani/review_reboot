from restaurant.settings import credentials

POSTGIS_VERSION = (2, 1, 2)

DATABASES = {
    'default': credentials['database']
}
