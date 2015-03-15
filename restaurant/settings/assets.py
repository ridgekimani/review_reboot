# common settings for webassets module
import os
from restaurant.settings import DEBUG, BASE_DIR

ASSETS_MODULES = [
    'restaurant.assets'
]

ASSETS_DEBUG = False
ASSETS_CACHE = False
ASSETS_MANIFEST = False
if not DEBUG:
    ASSETS_AUTO_BUILD = False

ASSETS_ROOT = os.path.join(BASE_DIR, 'restaurant/static')
