from accounts import models as am
from . import models as m

def assign_facebook_invitation(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        facebook_id = response.get('id')
        for invite in am.Invite.objects.filter(via='facebook', ref=facebook_id):
            invite.invitee = user
            invite.save()
