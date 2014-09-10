from base import *
DEBUG = False
TEMPLATE_DEBUG = DEBUG
# this is the default backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
WORKON_HOME = path('/var/www/django')
VENV_ROOT  = WORKON_HOME/PROJ_NAME

WWW_ROOT  = VENT_ROOT/'public-www'
STATIC_ROOT = WWW_ROOT/'static'
MEDIA_ROOT  = WWW_ROOT/'media'
CACHE_ROOT  = WWW_ROOT/'cache'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': CACHE_ROOT,
    },
    'staticfiles': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'staticfiles-filehashes'
    }
}
