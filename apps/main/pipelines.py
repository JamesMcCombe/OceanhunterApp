from apps.accounts.models import Invite


def assign_facebook_invitation(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        facebook_id = response.get('id')
        for invite in Invite.objects.filter(via='facebook', ref=facebook_id):
            invite.invitee = user
            invite.save()


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        p = user.profile

        if not p.gender and response.get('gender'):
            p.gender = response.get('gender')

        p.save()
