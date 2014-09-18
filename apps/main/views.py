from collections import OrderedDict

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from annoying.decorators import render_to, ajax_request

from . import models as m
from . import forms as f

APP_NAME = 'main'


def T(t, ext='html'):
    return '{}/{}.{}'.format(APP_NAME, t, ext)


@render_to()
def home(request):
    ctx = {}
    if not request.user.is_authenticated():
        ctx['TEMPLATE'] = 'home.html'
    else:
        # XXX Currently no feeds actually coz there is only one type of feed: fish
        # so dont need to add a news feed model right now.
        ctx['feeds'] = m.Fish.objects.order_by('-create')
        ctx['TEMPLATE'] = 'feed.html'
    return ctx


@login_required
@render_to('feed.html')
def fish_enlarge(request, fish_id):
    ctx = {}
    ctx['enlarge'] = True
    ctx['feeds'] = [get_object_or_404(m.Fish, pk=fish_id)]
    return ctx


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
def myfish(request, user_id):
    if user_id == 'me' or int(user_id) == request.user.id:
        u = request.user
        possessive = 'My'
    else:
        u = get_object_or_404(m.User, pk=user_id)
        possessive = u.profile.gender == 'male' and 'His' or 'Her'

    species_list = OrderedDict()
    for fish in u.fish_set.order_by('-create'):
        species_list.setdefault(fish.species, [])
        species_list[fish.species].append(fish)

    for species, fishes in species_list.items():
        species.points = sum(f.points for f in fishes)

    return {
        'u': u,
        'species_list':species_list,
        'possessive': possessive,
    }


@login_required
@render_to('myfish_myteam.html')
def myteam(request, user_id):
    if user_id == 'me' or int(user_id) == request.user.id:
        u = request.user
        possessive = 'My'
    else:
        u = get_object_or_404(m.User, pk=user_id)
        possessive = u.profile.gender == 'male' and 'His' or 'Her'
    return {
        'u': u,
        'possessive': possessive,
    }


@login_required
@ajax_request
def ajax_new_comment(request):
    u = request.user
    F = f.CommentForm
    if request.method == 'POST':
        form = F(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = u
            comment.save()
            return {'status': 'success'}
        else:
            return {'status': 'error', 'errors': form.errors}
