from .base import *

DEBUG = True
THUMBNAIL_DEBUG = DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Updated path handling using pathlib
from pathlib import Path
WORKON_HOME = Path('~/venv').expanduser()
VENV_ROOT = WORKON_HOME / 'node'
WWW_ROOT = PROJ_ROOT / 'public-www'
STATIC_ROOT = WWW_ROOT / 'static'
MEDIA_ROOT = WWW_ROOT / 'media'

INTERNAL_IPS = ('127.0.0.1',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJ_ROOT / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',  # Backend engine for PostgreSQL
#         'NAME': 'django_crayfish',                    # Name of your PostgreSQL database
#         'USER': 'django_user',                    # PostgreSQL username
#         'PASSWORD': 'password123',               # PostgreSQL password
#         'HOST': '3.106.245.171',                       # Database host, 'localhost' if running locally
#         'PORT': '5432',                            # PostgreSQL default port
#     }
# }

SOCIAL_AUTH_FACEBOOK_KEY = '1492664544305345'
SOCIAL_AUTH_FACEBOOK_SECRET = '93a9494c3e3cfbe0e2a3ae952d51a2e6'

X_FRAME_OPTIONS = "ALLOW-FROM https://apps.facebook.com/1505895249648941"

ADCODE_CACHE_TIMEOUT = 10  # seconds

SITE_URL = 'http://localhost:8000'
