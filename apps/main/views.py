from collections import OrderedDict
from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template import Context, loader
from django.core.mail import EmailMessage

from annoying.decorators import render_to, ajax_request
from annoying.functions import get_object_or_None

from dateutil.relativedelta import relativedelta

from accounts import models as am
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
    u = request.user
    existing_team = get_object_or_None(am.Team, users=u)
    isadmin = existing_team and existing_team.admin == u
    isfull = existing_team and existing_team.users.count() == 4

    if existing_team and (not isadmin or isfull):
        messages.error(request, 'Sorry only admin can invite new member.')
        return redirect('home')

    return {'existing_team': existing_team}


@login_required
@render_to('invite_email.html')
def invite_email(request):
    """I know this code of invitation is shit. Even me dont wanna see it again. Dont blame me."""
    u = request.user

    existing_team = get_object_or_None(am.Team, admin=u)

    F = f.TeamForm
    if request.method == 'GET':
        form = F()
    else:
        if not existing_team:
            form = F(request.POST)
            if not form.is_valid():
                return {'form': form}

            team = form.save(commit=False)
            team.admin = u
            team.save()
            team.users = [u]
            team.recalculate_points()
            existing_team = team

        emails = request.POST.getlist('email')
        emails = [email.strip() for email in emails if email.strip()]
        for email in emails:
            email_user = get_object_or_None(am.User, email=email)
            # already in a team can not invite
            if email_user and get_object_or_None(am.Team, users=email_user):
                continue
            data = dict(inviter=u, team=existing_team, via='email', ref=email, status='new')
            existing_invite = get_object_or_None(am.Invite, **data)

            if not existing_invite:
                invite = am.Invite(**data)
                invite.save()
                # this email user already our user
                if email_user:
                    invite.invitee = email_user
                    invite.save()
                subject = "%s %s invite you to join the team %s" % \
                    (u.first_name, u.last_name, existing_team.name)
                # TODO make a real email
                t = loader.get_template('emails/invitation.html')
                c = Context({'subject': subject, 'user': u, 'team': existing_team})
                html_content = t.render(c)
                msg = EmailMessage(subject, html_content, 'from@example.com', [email])
                msg.content_subtype = "html"
                msg.send()

        if len(emails) > 1:
            messages.success(request, 'Invites have been sent.')
        elif len(emails) == 1:
            messages.success(request, 'Invite has been sent.')

        if u.profile.is_new():
            return redirect('myfish_new')
        else:
            return redirect('invite')

    return {
        'form': form,
        'existing_team': existing_team,
    }


@login_required
@render_to('invite_facebook.html')
def invite_facebook(request):
    u = request.user

    existing_team = get_object_or_None(am.Team, admin=u)
    if existing_team:
        link = facebook_invite_link(request, existing_team)
        return redirect(link)

    F = f.TeamForm
    if request.method == 'GET':
        form = F()
    else:
        form = F(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.admin = u
            team.save()
            team.users = [u]
            team.recalculate_points()
            link = facebook_invite_link(request, team)
            return redirect(link)
    return {'form': form}


@login_required
def facebook_save_invitee(request):
    u = request.user
    team = get_object_or_404(am.Team, admin=u)

    facebook_ids = [v for k, v in request.GET.items() if k.startswith('to[') and k.endswith(']')]
    for id in facebook_ids:
        fb_user = get_object_or_None(am.User, social_auth__provider='facebook', social_auth__uid=id)
        # already in a team can not invite
        if fb_user and get_object_or_None(am.Team, users=fb_user):
            continue

        data = dict(inviter=u, team=team, via='facebook', ref=id, status='new')
        existing_invite = get_object_or_None(am.Invite, **data)
        if not existing_invite:
            invite = am.Invite(**data)
            invite.save()
            # this facebook user already our user
            if fb_user:
                invite.invitee = fb_user
                invite.save()

    if len(facebook_ids) > 1:
        messages.success(request, 'Invites have been sent.')
    elif len(facebook_ids) == 1:
        messages.success(request, 'Invite has been sent.')

    if u.profile.is_new():
        return redirect('myfish_new')
    else:
        return redirect('invite')


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
            team = get_object_or_None(am.Team, users=u)
            if team:
                team.recalculate_points()
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

    if request.method == 'POST':
        do_team_invite_post(request)

    team = get_object_or_None(am.Team, users=u)
    possessive_team = 'My'
    if team and request.user not in team.users.all():
        possessive_team = possessive

    invite = get_object_or_None(am.Invite, invitee=request.user, team=team, status='new')

    return {
        'u': u,
        'possessive': possessive,
        'team': team,
        'invite': invite,
        'possessive_team': possessive_team,
    }


@login_required
@render_to('myfish_myteam.html')
def team_alone(request, team_id):
    if request.method == 'POST':
        do_team_invite_post(request)

    u = request.user
    team = get_object_or_404(am.Team, pk=team_id)
    if request.user in team.users.all():
        possessive_team = 'My'
    else:
        possessive_team = 'Open'

    invite = get_object_or_None(am.Invite, invitee=u, team=team, status='new')

    return {
        'team': team,
        'team_alone': True,
        'invite': invite,
        'possessive_team': possessive_team,
    }


def do_team_invite_post(request):
    u = request.user
    action = request.POST.get('action')
    invite_id = request.POST.get('invite_id')
    invite = get_object_or_None(am.Invite, pk=invite_id, status='new')

    if not invite:
        return

    if action == 'join':
        invite.status = 'accepted'
        invite.accept = datetime.now()
        invite.team.users.add(u)
        invite.team.recalculate_points()
        messages.success(request, 'Congratulation! Now you are member of %s!' % invite.team.name)
    elif action == 'reject':
        invite.status = 'read'

    invite.read = datetime.now()
    invite.save()


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


@render_to('leaderboard.html')
def leaderboard(request):
    PERPAGE = 15
    p = request.GET.get('p', 1)
    F = f.FilterForm

    # make a copy for modify it
    form_data = request.GET.copy()

    # unit always required and default is solo
    if not form_data.get('unit'):
        form_data['unit'] = 'solo'

    # area and city can not be setup both
    if form_data.get('area') and form_data.get('city'):
        del form_data['city']

    if form_data.get('unit') == 'solo' and form_data.get('team_kind'):
        del form_data['team_kind']

    form = F(form_data or None)
    if form.is_valid():
        filters = form.cleaned_data

        if filters['species']:
            type = 'fish'
            q = m.Fish.objects \
                .filter(species=filters['species']) \
                .order_by('-points')
            if filters['city']:
                q = q.filter(user__profile__city=filters['city'])
            if filters['area']:
                q = q.filter(user__profile__area=filters['area'])

            junior_dob = date.today() - relativedelta(years=14)
            if filters['age'] == 'junior':
                q = q.filter(user__profile__dob__lt=junior_dob)
            elif filters['age'] == 'open':
                q = q.filter(user__profile__dob__gte=junior_dob)

            if filters['gender']:
                q = q.filter(user__profile__gender=filters['gender'])

        elif filters['unit'] == 'team':
            type = 'team'
            q = am.Team.objects \
                .exclude(points=0) \
                .order_by('-points')

            if filters['team_kind']:
                q = q.filter(kind=filters['team_kind'])

        else: # elif filters['unit'] == 'team'
            type = 'solo'
            q = m.User.objects \
                .exclude(profile__points=0) \
                .order_by('-profile__points')

            if filters['city']:
                q = q.filter(profile__city=filters['city'])
            if filters['area']:
                q = q.filter(profile__area=filters['area'])

            junior_dob = date.today() - relativedelta(years=14)
            if filters['age'] == 'junior':
                q = q.filter(profile__dob__lt=junior_dob)
            elif filters['age'] == 'open':
                q = q.filter(profile__dob__gte=junior_dob)

            if filters['gender']:
                q = q.filter(profile__gender=filters['gender'])

        paginator = Paginator(q, PERPAGE)

        page = paginator.page(p)
        start = PERPAGE * (p - 1)

        radios = (form[name] for name in ['area', 'unit', 'team_kind', 'age', 'gender'])
        return {
            'page': page,
            'start': start,
            'form': form,
            'type': type,
            'radios': radios,
        }
    else:
        # for debug only
        # normally it should not have any errors
        print form.errors


def facebook_invite_link(request, team):
    app_id = settings.SOCIAL_AUTH_FACEBOOK_KEY
    schema = request.is_secure() and 'https' or 'http'
    base_url = "%s://%s" % (schema, request.get_host())

    redirect_uri = base_url + reverse('facebook_save_invitee')
    message = "Join my team %s please!" % team.name

    return "http://www.facebook.com/dialog/apprequests?" \
            "app_id=%(app_id)s" \
            "&message=%(message)s" \
            "&redirect_uri=%(redirect_uri)s" % locals()
