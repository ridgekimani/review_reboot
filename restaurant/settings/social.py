from restaurant.settings import credentials


SOCIAL_AUTH_FACEBOOK_KEY = credentials['SOCIAL_AUTH_FACEBOOK_KEY']
SOCIAL_AUTH_FACEBOOK_SECRET = credentials['SOCIAL_AUTH_FACEBOOK_SECRET']

# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = credentials['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = credentials['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']

# SOCIAL_AUTH_GOOGLE_OAUTH2_USE_DEPRECATED_API = True
# SOCIAL_AUTH_GOOGLE_PLUS_USE_DEPRECATED_API = True

# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# for more backends check http://django-social-auth.readthedocs.org/en/latest/configuration.html
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "social.backends.facebook.FacebookOAuth2",
    "social.backends.google.GoogleOpenIdConnect",
    'social.backends.google.GoogleOAuth2'
)


SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name']


'''SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    #'venues.pipeline.social_profile_link',
)'''
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    #'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)



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
# ACCOUNT_OPEN_SIGNUP = True
# ACCOUNT_EMAIL_UNIQUE = True
# ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
# ACCOUNT_LOGIN_REDIRECT_URL = "home"
# ACCOUNT_LOGOUT_REDIRECT_URL = "home"
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
