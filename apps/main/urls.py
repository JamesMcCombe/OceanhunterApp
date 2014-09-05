from django.conf.urls import patterns, url

urlpatterns = patterns('main.views',
    url(r'^$', 'home', name='home'),
    url(r'^go/$', 'go', name='go'),
    url(r'^invite/$', 'invite', name='invite'),
    url(r'^invite/email/$', 'invite_email', name='invite_email'),
)

