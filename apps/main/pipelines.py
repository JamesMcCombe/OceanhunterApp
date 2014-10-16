from accounts import models as am
from . import models as m

def assign_facebook_invitation(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        facebook_id = response.get('id')
        for invite in am.Invite.objects.filter(via='facebook', ref=facebook_id):
            invite.invitee = user
            invite.save()


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        """
        # response is a dict like this
        response = {
            u'first_name': u'Sam',
            u'last_name': u'Letuchysky',
            u'middle_name': u'Amffjghagbdj',
            u'name': u'Sam Amffjghagbdj Letuchysky',
            'access_token': u'CAAAmo...x2shFyo',
            u'gender': u'male',
            'expires': u'5171223',
            u'age_range': {u'min': 21},
            u'email': u'sam_jlipwhr_letuchysky@tfbnw.net',
            u'link': u'https://www.facebook.com/app_scoped_user_id/1553583724871873/',
            u'updated_time': u'2014-10-07T02:26:13+0000',
            u'id': u'1553583724871873',
            u"location": {
                u"id": u"112254842134171",
                u"name": u"Auckland, New Zealand"
            }
        }"""
        p = user.profile

        if not p.gender and response.get('gender'):
            p.gender = response.get('gender')

        p.save()
