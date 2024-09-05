from .base import *

DEBUG = True

# Django 4.x does not have TEMPLATE_DEBUG, it is unified with DEBUG
# THUMBNAIL_DEBUG can also be removed or handled based on the DEBUG flag
THUMBNAIL_DEBUG = DEBUG

# Use console backend for email in development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Define paths for virtual environments and static/media files
WORKON_HOME = Path('~/venv').expanduser()
VENV_ROOT = WORKON_HOME / 'node'
WWW_ROOT = PROJ_ROOT / 'public-www'
STATIC_ROOT = WWW_ROOT / 'static'
MEDIA_ROOT = WWW_ROOT / 'media'

# Define internal IPs for Django Debug Toolbar or other development tools
INTERNAL_IPS = ('127.0.0.1',)

# Configure the development database using SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(PROJ_ROOT / 'db.sqlite3'),
    }
}

# Facebook social authentication keys for development
SOCIAL_AUTH_FACEBOOK_KEY = '1492664544305345'
SOCIAL_AUTH_FACEBOOK_SECRET = '93a9494c3e3cfbe0e2a3ae952d51a2e6'
SOCIAL_AUTH_FACEBOOK_APP_KEY = '1492664544305345'
SOCIAL_AUTH_FACEBOOK_APP_SECRET = '93a9494c3e3cfbe0e2a3ae952d51a2e6'

# Frame options for embedding within Facebook
X_FRAME_OPTIONS = "ALLOW-FROM https://apps.facebook.com/1492664544305345"

# Ad code cache timeout setting
ADCODE_CACHE_TIMEOUT = 10  # seconds

# Site URL for development
SITE_URL = 'http://oceanhunter.local.node.co.nz:8000'
