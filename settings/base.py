import sys
from path import path
from os.path import dirname,abspath
HERE = path(dirname(abspath(__file__)))
PROJ_ROOT = BASE_DIR = HERE.parent
PROJ_NAME = PROJ_ROOT.name
APPS_ROOT = PROJ_ROOT/'apps'

sys.path.insert(0,PROJ_ROOT)
sys.path.insert(0,APPS_ROOT)

# to generate nginx conf
SERVER_NAME = 'example.com'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@w@4gg7^dy9z3(r%n0b&*rr)4cf0-b$=hpsyx5qo0r4l3b=i$8'

ADMINS = (
    ('Node Developers', 'developers@node.co.nz'),
)

MANAGERS = (
    ('Mike', 'mike@oceanhunter.co.nz'),
    ('James', 'james@node.co.nz'),
)

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'annoying',
    'django_extensions',
    'sekizai',
    'social.apps.django_app.default',
    'sorl.thumbnail',
    'adcode',

    'accounts',
    'main',
    'pages',
)


AUTHENTICATION_BACKENDS = (
    'accounts.backends.EmailAuthBackend',
    'social.backends.facebook.Facebook2OAuth2',
    'social.backends.facebook.Facebook2AppOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'sekizai.context_processors.sekizai',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'adcode.context_processors.current_placements',
    'main.context_processors.facebook_app_id',
    'main.context_processors.unread_invites',
    'main.context_processors.baseurl',
)

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is were emails and domains whitelists are applied (if
    # defined).
    'social.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social.pipeline.social_auth.social_user',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social.pipeline.user.get_username',

    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social.pipeline.mail.mail_validation',

    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    'social.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social.pipeline.user.create_user',

    # Create the record that associated the social account with this user.
    'social.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social.pipeline.user.user_details',

    # Assign to existing invitation
    'main.pipelines.assign_facebook_invitation',

    # Save profile
    'main.pipelines.save_profile',
)

SOCIAL_AUTH_USER_MODEL = 'auth.User'
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['email', 'first_name', 'last_name', 'gender']
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

SOCIAL_AUTH_FACEBOOK_KEY = '1492664544305345'
SOCIAL_AUTH_FACEBOOK_SECRET = '93a9494c3e3cfbe0e2a3ae952d51a2e6'
SOCIAL_AUTH_FACEBOOK_APP_KEY = '1492664544305345'
SOCIAL_AUTH_FACEBOOK_APP_SECRET = '93a9494c3e3cfbe0e2a3ae952d51a2e6'
SOCIAL_AUTH_FACEBOOK_APP_NAMESPACE = 'nodeoceanhunter'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False
#SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_location', 'user_birthday']
SOCIAL_AUTH_FACEBOOK_SCOPE = ['public_profile', 'email']

X_FRAME_OPTIONS = "ALLOW-FROM https://apps.facebook.com/nodeoceanhunter"

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

TIME_ZONE = 'Pacific/Auckland'
USE_TZ = True

USE_I18N = True
USE_L10N = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    PROJ_ROOT/"static",
)

TEMPLATE_DIRS = (
    PROJ_ROOT/"templates",
)

FIXTURE_DIRS = (
    PROJ_ROOT/"fixtures",
)

EMAIL_HOST = 'smtp.officemail.co.nz'
SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'Ocean Hunter <comp@oceanhunter.co.nz>'
EMAIL_HOST_USER = 'oceanhunter06'
EMAIL_HOST_PASSWORD = '123455' # TODO: fill this in local.py
EMAIL_SUBJECT_PREFIX='[%s]' % PROJ_NAME
EMAIL_USE_SSL = True
EMAIL_PORT = 465

ADCODE_PLACEHOLDER_TEMPLATE = '//placehold.it/{width}x{height}'
