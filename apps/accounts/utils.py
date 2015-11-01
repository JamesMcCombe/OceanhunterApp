from django.conf import settings
from django.utils import timezone

from open_facebook import OpenFacebook

from apps.accounts.models import FacebookAdminToken


def renew_facebook_admin_token():
    current_token = FacebookAdminToken.objects.last()

    if current_token.obtained > (timezone.now() - timezone.timedelta(days=14)):
        return

    # obtained two weeks ago, time to renew

    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': settings.SOCIAL_AUTH_FACEBOOK_APP_KEY,
        'client_secret': settings.SOCIAL_AUTH_FACEBOOK_SECRET,
        'fb_exchange_token': current_token.access_token
    }

    graph = OpenFacebook()
    resp = graph.get('oauth/access_token', **params)

    FacebookAdminToken(resp['access_token']).save()
