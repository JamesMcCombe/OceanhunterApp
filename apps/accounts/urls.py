from django.conf.urls import patterns, url
from path import path
from os.path import abspath, dirname

APP_ROOT = path(dirname(abspath(__file__)))
APP_NAME = APP_ROOT.name

urlpatterns = patterns('%s.views' % APP_NAME,
                       # url(r'^signup/$', 'signup', name='signup'),
                       # url(r'^signup/extra_profile/$', 'extra_profile', name='extra_profile'),
                       url(r'^login/$', 'login', name='login'),
                       url(r'^logout/$', 'logout', name='logout'),
                       # url(r'^fbuser/$', 'fbuser', name='fbuser'),
                       )

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^password/change/$', 'password_change', name="password_change"),
    url(r'^password/change/done/$', 'password_change_done', name="password_change_done"),
    url(r'^password/reset/$', 'password_reset', {'html_email_template_name': 'registration/password_reset_email_html-inline.html'}, name="password_reset"),
    url(r'^password/reset/done/$', 'password_reset_done', name='password_reset_done'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'password_reset_confirm', name="password_reset_confirm"),
    url(r'^password/done/$', 'password_reset_complete', name="password_reset_complete")
)
