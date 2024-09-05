from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, re_path, path
from django.contrib import admin
from apps.pages import views as pages_views

urlpatterns = [
    re_path(r'^accounts/', include('accounts.urls')),
    re_path(r'^social/', include('social_django.urls', namespace='social')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^privacy-policy$', pages_views.page, {'slug': 'privacy-policy'}, name='privacy-policy'),
    re_path(r'^rules-conditions$', pages_views.page, {'slug': 'rules-conditions'}, name='rules-conditions'),
    re_path(r'', include('main.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
