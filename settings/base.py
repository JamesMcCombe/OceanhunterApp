import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ_ROOT = BASE_DIR = HERE.parent
PROJ_NAME = PROJ_ROOT.name
APPS_ROOT = PROJ_ROOT / 'apps'

sys.path.insert(0, str(PROJ_ROOT))
sys.path.insert(0, str(APPS_ROOT))

# to generate nginx conf
SERVER_NAME = 'example.com'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-default-secret-key')

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
    # 'raven.contrib.django.raven_compat',  # Replace with sentry_sdk
    'debug_toolbar',

    'apps.accounts',
    'apps.main',
    'apps.pages',
]

AUTHENTICATION_BACKENDS = (
    'accounts.backends.EmailAuthBackend',
    'social_core.backends.facebook.FacebookOAuth2', 
    'social_core.backends.facebook.FacebookAppOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJ_ROOT / "templates"],
        'APP_DIRS': True,
        "OPTIONS": {
            "context_processors": [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.template.context_processors.tz',
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



SOCIAL_AUTH_PIPELINE = [
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    # 'social_core.pipeline.mail.mail_validation',  # If needed
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'main.pipelines.assign_facebook_invitation',
    'main.pipelines.save_profile',
]

SOCIAL_AUTH_USER_MODEL = 'auth.User'
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['email', 'first_name', 'last_name', 'gender']
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('SOCIAL_AUTH_FACEBOOK_KEY', '1492664544305345')
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('SOCIAL_AUTH_FACEBOOK_SECRET', '93a9494c3e3cfbe0e2a3ae952d51a2e6')
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

STATICFILES_DIRS = [
    PROJ_ROOT / "static",
]

FIXTURE_DIRS = [
    PROJ_ROOT / "fixtures",
]

SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'Ocean Hunter <info@oceanhunter.node.co.nz>'

ADCODE_PLACEHOLDER_TEMPLATE = '//placehold.it/{width}x{height}'

# Use sentry_sdk instead of Raven
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration

# sentry_sdk.init(
#     dsn=os.getenv('SENTRY_DSN', 'your-sentry-dsn'),
#     integrations=[DjangoIntegration()],
#     traces_sample_rate=1.0,
#     send_default_pii=True
# )

THUMBNAIL_PADDING_COLOR = '#000000'



SITE_URL = 'http://oceanhunter.node.co.nz'
LOGIN_URL = '/go/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
