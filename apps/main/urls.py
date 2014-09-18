from django.conf.urls import patterns, url

urlpatterns = patterns('main.views',
    url(r'^$', 'home', name='home'),
    url(r'^go/$', 'go', name='go'),

    url(r'^invite/$', 'invite', name='invite'),
    url(r'^invite/email/$', 'invite_email', name='invite_email'),

    url(r'^fish/$', 'myfish', name='myfish'),
    url(r'^team/$', 'myteam', name='myteam'),
    url(r'^fish/new/$', 'myfish_new', name='myfish_new'),
    url(r'^feed/(?P<fish_id>\d+)/$', 'fish_enlarge', name='fish_enlarge'),

    url(r'^ajax/newcomment/$', 'ajax_new_comment', name='ajax_new_comment'),
)

