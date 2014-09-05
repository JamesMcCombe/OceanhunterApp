from django.conf.urls import patterns, url

urlpatterns = patterns('pages.views',
    url(r'^(?P<slug>.+)$', 'page', name='page'),
)

