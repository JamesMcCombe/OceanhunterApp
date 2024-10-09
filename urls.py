from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
from apps.pages.views import page

urlpatterns = [
    path('accounts/', include('apps.accounts.urls')),
    path('social/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path('privacy-policy/', page, {'slug': 'privacy-policy'}, name='privacy-policy'),
    path('rules-conditions/', page, {'slug': 'rules-conditions'}, name='rules-conditions'),
    path('', include('apps.main.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
