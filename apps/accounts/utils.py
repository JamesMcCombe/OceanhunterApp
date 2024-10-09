from django.conf import settings
from django.utils import timezone
from social_core.backends.facebook import FacebookOAuth2
from apps.accounts.models import FacebookAdminToken


def renew_facebook_admin_token():
    current_token = FacebookAdminToken.objects.last()

    if current_token and current_token.obtained > (timezone.now() - timezone.timedelta(days=14)):
        return

    # Renew the token as it was obtained more than 14 days ago
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': settings.SOCIAL_AUTH_FACEBOOK_KEY,
        'client_secret': settings.SOCIAL_AUTH_FACEBOOK_SECRET,
        'fb_exchange_token': current_token.access_token
    }

    backend = FacebookOAuth2()
    response = backend.get_json('https://graph.facebook.com/oauth/access_token', params=params)

    # Save the new token
    FacebookAdminToken(access_token=response['access_token']).save()
