from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to, ajax_request

from . import models as m

APP_NAME = 'main'


def T(t, ext='html'):
    return '{}/{}.{}'.format(APP_NAME, t, ext)


@render_to('home.html')
def home(request):
    return {}


@render_to('go.html')
def go(request):
    return {}


@login_required
@render_to('invite.html')
def invite(request):
    return {}


@login_required
@render_to('invite_email.html')
def invite_email(request):
    return {}


@login_required
@render_to('myfish_new.html')
def myfish_new(request):
    species = m.Species.objects.all()
    return {'species': species}

