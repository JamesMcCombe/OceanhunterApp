from django.conf import settings
from django.contrib.auth.models import User
from apps.accounts.models import Invite, Team

def facebook_app_id(request):
    return {'FACEBOOK_APP_ID': settings.SOCIAL_AUTH_FACEBOOK_KEY}

def unread_invites(request):
    u = request.user
    if u.is_authenticated and not u.team_set.exists():
        unread_invites = Invite.objects.filter(invitee=u, status='new', inviter__profile__division=u.profile.division)
        return {'unread_invites': unread_invites}
    return {}

def statistics(request):
    u = request.user
    if u.is_staff:
        return {
            'USERS_COUNT': User.objects.count(),
            'TEAMS_COUNT': Team.objects.count(),
            'INVITES_COUNT': Invite.objects.count(),
            'PENDING_INVITES_COUNT': Invite.objects.filter(status="new").count(),
        }
    return {}

def baseurl(request):
    scheme = 'https://' if request.is_secure() else 'http://'
    return {'BASE_URL': scheme + request.get_host()}