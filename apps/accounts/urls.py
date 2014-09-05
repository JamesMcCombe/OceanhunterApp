from django.conf.urls import patterns, url
from path import path
from os.path import abspath, dirname

APP_ROOT = path(dirname(abspath(__file__)))
APP_NAME = APP_ROOT.name

urlpatterns = patterns('%s.views' % APP_NAME,
                       url(r'^signup/$', 'signup', name='signup'),
                       url(r'^login/$', 'login', name='login'),
                       url(r'^logout/$', 'logout', name='logout'),
                       url(r'^fbuser/$', 'fbuser', name='fbuser'),
                       )
