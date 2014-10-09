from django.conf import settings
from accounts import models as am

def facebook_app_id(request):
    return {'FACEBOOK_APP_ID': settings.SOCIAL_AUTH_FACEBOOK_KEY}


def unread_invites(request):
    u = request.user
    if u.is_authenticated():
        unread_invites = am.Invite.objects.filter(invitee=u, status='new')
        return {'unread_invites': unread_invites}
    else:
        return {}
