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

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'annoying',
    'django_extensions',
    'sekizai',
    'social.apps.django_app.default',
    'south',

    'accounts',
    'main',
    'pages',
)


AUTHENTICATION_BACKENDS = (
    'accounts.backends.EmailAuthBackend',
    'social.backends.facebook.Facebook2OAuth2',
    'django.contrib.auth.backends.ModelBackend',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'sekizai.context_processors.sekizai',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

SOCIAL_AUTH_USER_MODEL = 'auth.User'
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['email', 'first_name', 'last_name']
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

SOCIAL_AUTH_FACEBOOK_KEY = '1492664544305345'
SOCIAL_AUTH_FACEBOOK_SECRET = '93a9494c3e3cfbe0e2a3ae952d51a2e6'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
#SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/TODO'
#SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_location', 'user_birthday']
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

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

EMAIL_HOST='smtp.gmail.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL = EMAIL_HOST_USER = 'node@node.co.nz'
EMAIL_HOST_PASSWORD='123456' # TODO: fill this in local.py
EMAIL_SUBJECT_PREFIX='[%s]' % PROJ_NAME
EMAIL_USE_TLS=True
EMAIL_PORT=587
