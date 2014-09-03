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

    'accounts',
    'main',
)


AUTHENTICATION_BACKENDS = (
    'accounts.backends.EmailAuthBackend',
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
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

TIME_ZONE = 'Pacific/Auckland'
USE_TZ = False

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
