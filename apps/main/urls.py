from django.conf.urls import patterns, url

urlpatterns = patterns('main.views',
    url(r'^$', 'home', name='home'),
    url(r'^go/$', 'go', name='go'),
    url(r'^invite/$', 'invite', name='invite'),
)

