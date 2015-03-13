from restaurant.settings import credentials


SOCIAL_AUTH_FACEBOOK_KEY = credentials['SOCIAL_AUTH_FACEBOOK_KEY']
SOCIAL_AUTH_FACEBOOK_SECRET = credentials['SOCIAL_AUTH_FACEBOOK_SECRET']

# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# for more backends check http://django-social-auth.readthedocs.org/en/latest/configuration.html
AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOpenIdConnect',
    'django.contrib.auth.backends.ModelBackend',
    'account.auth_backends.UsernameAuthenticationBackend',
)


SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name']


# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'redkovich@gmail.com'
# EMAIL_HOST_PASSWORD = 'vkiofcumunkmixrj'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
#
# FIXTURE_DIRS = [
# os.path.join(BASE_DIR, "fixtures"),
# ]
#
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
ACCOUNT_LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
