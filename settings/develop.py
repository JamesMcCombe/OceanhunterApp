from base import *
DEBUG = True
TEMPLATE_DEBUG = DEBUG
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

