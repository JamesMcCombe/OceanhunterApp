from django.conf.urls import patterns, url
from path import path
from os.path import abspath,dirname

APP_ROOT = path(dirname(abspath(__file__)))
APP_NAME = APP_ROOT.name

urlpatterns = patterns('%s.views' % APP_NAME,
    url(r'^index/$', 'index', name='index'),
)

