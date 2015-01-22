from base import *
DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
WORKON_HOME = path('~/venv')
VENV_ROOT  = WORKON_HOME/'node'
WWW_ROOT  = PROJ_ROOT/'public-www'
STATIC_ROOT = WWW_ROOT/'static'
MEDIA_ROOT = WWW_ROOT/'media'

INTERNAL_IPS = ('127.0.0.1',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJ_ROOT/'db.sqlite'
    }
}

SOCIAL_AUTH_FACEBOOK_KEY = '1505895249648941'
SOCIAL_AUTH_FACEBOOK_SECRET = 'cb92886f51ccb2759e75e3c6e2261171'
SOCIAL_AUTH_FACEBOOK_APP_KEY = '1505895249648941'
SOCIAL_AUTH_FACEBOOK_APP_SECRET = 'cb92886f51ccb2759e75e3c6e2261171'
X_FRAME_OPTIONS = "ALLOW-FROM https://apps.facebook.com/1505895249648941"


ADCODE_CACHE_TIMEOUT = 10 # seconds

SITE_URL = 'http://oceanhunter.local.node.co.nz:8000'
