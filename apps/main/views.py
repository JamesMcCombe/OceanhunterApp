from collections import OrderedDict

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from annoying.decorators import render_to, ajax_request

from . import models as m
from . import forms as f

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
    u = request.user
    F = f.FishForm
    if request.method == 'GET':
        form = F()
    else:
        print request.POST, request.FILES
        form = F(data=request.POST, files=request.FILES)
        if form.is_valid():
            fish = form.save(commit=False)
            fish.user = u
            fish.save()
            u.profile.recalculate_points()
            return redirect('home')
    ctx = {'form': form}

    return ctx


@login_required
@render_to('myfish.html')
def myfish(request):
    u = request.user
    species_list = OrderedDict()
    for fish in u.fish_set.order_by('-create'):
        species_list.setdefault(fish.species, [])
        species_list[fish.species].append(fish)

    for species, fishes in species_list.items():
        species.points = sum(f.points for f in fishes)

    return {'user': u, 'species_list':species_list}

