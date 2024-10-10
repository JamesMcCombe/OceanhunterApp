import sys, os
from pathlib import Path
from os.path import dirname, abspath

HERE = Path(dirname(abspath(__file__)))
PROJ_ROOT = BASE_DIR = HERE.parent
PROJ_NAME = PROJ_ROOT.name
APPS_ROOT = PROJ_ROOT / 'apps'

sys.path.insert(0, str(PROJ_ROOT))
sys.path.insert(0, str(APPS_ROOT))

# to generate nginx conf
SERVER_NAME = 'example.com'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@w@4gg7^dy9z3(r%n0b&*rr)4cf0-b$=hpsyx5qo0r4l3b=i$8'

ADMINS = (
    ('Ilian Iliev', 'ilian@ilian.io'),
    ('info', 'info@oceanhunter.node.co.nz'),
)

MANAGERS = (
    ('Mike', 'mike@oceanhunter.co.nz'),
    ('James', 'james@node.co.nz'),
)

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
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
    'social_django',
    'sorl.thumbnail',
    'adcode',
    'debug_toolbar',
    'apps.accounts',
    'apps.main',
    'apps.pages',
]

AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailAuthBackend',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJ_ROOT / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'adcode.context_processors.current_placements',
                'main.context_processors.facebook_app_id',
                'main.context_processors.unread_invites',
                'main.context_processors.statistics',
                'main.context_processors.baseurl',
            ],
        },
    },
]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',  # This line is crucial if you want to auto-associate users by email
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('SOCIAL_AUTH_FACEBOOK_KEY', '1492664544305345')
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('SOCIAL_AUTH_FACEBOOK_SECRET', '93a9494c3e3cfbe0e2a3ae952d51a2e6')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']  # Get user email
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}


SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SOCIAL_AUTH_FACEBOOK_SCOPE = ['public_profile', 'email']

X_FRAME_OPTIONS = "ALLOW-FROM https://apps.facebook.com/nodeoceanhunter"

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Pacific/Auckland'
USE_TZ = True
USE_I18N = True
USE_L10N = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    PROJ_ROOT / 'static',
]

FIXTURE_DIRS = [
    PROJ_ROOT / 'fixtures',
]

SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'Ocean Hunter <info@oceanhunter.node.co.nz>'

ADCODE_PLACEHOLDER_TEMPLATE = '//placehold.it/{width}x{height}'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/var/apps/log/oceanhunter/debug.log',
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'include_html': True
#         },
#     },
#     'loggers': {
#         'oceanhunter': {
#             'handlers': ['file', 'mail_admins'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#     }
# }

SITE_URL = 'http://kingofcrays.co.nz/'
LOGIN_URL = '/go/'

SITE_ID = 1

