from collections import OrderedDict
from datetime import datetime, date
from itertools import chain

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, mail_managers
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Sum, Count
from django.shortcuts import redirect, get_object_or_404
from django.template import RequestContext, loader

from open_facebook import OpenFacebook
from apps.accounts.models import FacebookAdminToken
from social_core.utils import sanitize_redirect
from social_core.backends.facebook import FacebookOAuth2
from django.http import HttpResponseRedirect

from annoying.decorators import render_to, ajax_request
from annoying.functions import get_object_or_None

from dateutil.relativedelta import relativedelta

from apps.accounts.models import Team, Invite
from apps.main import models as m
from apps.main import forms as f


APP_NAME = 'main'


def T(t, ext='html'):
    return '{}/{}.{}'.format(APP_NAME, t, ext)

@login_required
@render_to()
def home(request):
    if not request.user.profile.profile_completed:
        return redirect('extra_profile')
    ctx = {}
    PERPAGE = 8
    EXAMPLE_FISH_ID = 1
    q = m.Fish.objects.exclude(pk=EXAMPLE_FISH_ID).order_by('-create')
    paginator = Paginator(q, PERPAGE)
    p = request.GET.get('p', 1)
    page = paginator.page(p)
    start = PERPAGE * (int(p) - 1)
    feeds = page.object_list
    if p == 1:
        feeds = chain(m.Fish.objects.filter(pk=EXAMPLE_FISH_ID), feeds)
    ctx['page'] = page
    ctx['start'] = start
    ctx['feeds'] = feeds
    ctx['TEMPLATE'] = 'feed.html'
    return ctx


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
    if not request.user.profile.profile_completed:
        return redirect('extra_profile')
    u = request.user
    existing_team = get_object_or_None(Team, users=u)
    isadmin = existing_team and existing_team.admin == u
    isfull = existing_team and existing_team.users.count() == 4

    if existing_team and (not isadmin or isfull):
        messages.error(request, 'Sorry only admin can invite new member.')
        return redirect('home')

    if date.today() >= date(2017, 2, 1):
        messages.error(request, 'Sorry you cannot create team after 1st of February')
        return redirect('home')

    return {'existing_team': existing_team}


@login_required
@render_to('invite_email.html')
def invite_email(request):
    if not request.user.profile.profile_completed:
        return redirect('extra_profile')
    u = request.user

    existing_team = get_object_or_None(Team, admin=u)

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
            team.users.set([u])
            existing_team = team

        emails = request.POST.getlist('email')
        emails = [email.strip() for email in emails if email.strip()]
        success_invitations = []
        for email in emails:
            email_user = get_object_or_None(User, email=email)
            if email_user and get_object_or_None(Team, users=email_user):
                messages.error(request, 'You cannot invite %s who already has a team.' % email)
                continue
            success_invitations.append(email)
            data = dict(inviter=u, team=existing_team, via='email', ref=email, status='new')
            existing_invite = get_object_or_None(Invite, **data)

            if not existing_invite:
                invite = Invite(**data)
                invite.save()
                if email_user:
                    invite.invitee = email_user
                    invite.save()
                subject = "%s %s has invited you to join the team %s" % \
                    (u.first_name, u.last_name, existing_team.name)
                t = loader.get_template('emails/invitation-inline.html')
                c = RequestContext(request, {'subject': subject, 'user': u, 'team': existing_team,
                                             'invitation_code': invite.key})
                html_content = t.render(c)
                msg = EmailMessage(subject, html_content, settings.DEFAULT_FROM_EMAIL, [email])
                msg.content_subtype = "html"
                msg.send()

        if len(success_invitations) > 1:
            messages.success(request, 'Invites have been sent.')
        elif len(success_invitations) == 1:
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
    if not request.user.profile.profile_completed:
        return redirect('extra_profile')
    u = request.user

    existing_team = get_object_or_None(Team, admin=u)
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
            team.users.set([u])
            link = facebook_invite_link(request, team)
            return redirect(link)
    return {'form': form}


@login_required
def facebook_save_invitee(request):
    u = request.user
    team = get_object_or_404(Team, admin=u)

    facebook_ids = [v for k, v in request.GET.items() if k.startswith('to[') and k.endswith(']')]
    for id in facebook_ids:
        fb_user = get_object_or_None(User, social_auth__provider='facebook', social_auth__uid=id)
        if fb_user and get_object_or_None(Team, users=fb_user):
            continue

        data = dict(inviter=u, team=team, via='facebook', ref=id, status='new')
        existing_invite = get_object_or_None(Invite, **data)
        if not existing_invite:
            invite = Invite(**data)
            invite.save()
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
    if not request.user.profile.profile_completed:
        return redirect('extra_profile')

    u = request.user
    F = f.FishForm

    form = F(request, data=request.POST or None, files=request.FILES or None)
    if form.is_valid():
        fish = form.save(commit=False)
        fish.user = u
        fish.save()
        return redirect('home')

    species = form.fields['species'].queryset
    for s in species:
        s.count_of_user = m.Fish.objects.filter(user=u, species=s).count()
    ctx = {'form': form, 'species': species}

    return ctx


@login_required
@render_to('myfish.html')
def myfish(request, user_id):
    if user_id == 'me' or int(user_id) == request.user.id:
        u = request.user
        possessive = 'My'
        team = get_object_or_None(Team, users=u)
        if not team:
            possessive_team = 'Create'
        else:
            possessive_team = possessive
    else:
        u = get_object_or_404(User, pk=user_id)
        possessive = 'Their'
        possessive_team = possessive

    species_list = OrderedDict()
    for fish in u.fish_set.order_by('-points'):
        species_list.setdefault(fish.species, [])
        species_list[fish.species].append(fish)

    for species, fishes in species_list.items():
        species.points = sum(f.points for f in fishes)
        species.weight = sum(f.weight for f in fishes)

    return {
        'u': u,
        'species_list':species_list,
        'possessive': possessive,
        'possessive_team': possessive_team,
    }


@login_required
def myfish_delete(request):
    u = request.user
    if request.method == 'POST':
        fish_id = request.POST.get('id')
        fish = get_object_or_404(m.Fish, pk=fish_id, user=u)
        fish.delete()
        return redirect('home')


@login_required
@render_to('myfish_myteam.html')
def myteam(request, user_id):
    if user_id == 'me' or int(user_id) == request.user.id:
        u = request.user
        possessive = 'My'
    else:
        u = get_object_or_404(User, pk=user_id)
        possessive = u.profile.gender == 'male' and 'His' or 'Her'

    if request.method == 'POST':
        do_team_invite_post(request)

    team = get_object_or_None(Team, users=u)
    possessive_team = possessive
    if possessive == 'My' and not team:
        possessive_team = 'Create'

    invite = get_object_or_None(Invite, invitee=request.user, team=team, status='new')

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
    team = get_object_or_404(Team, pk=team_id)
    if request.user in team.users.all():
        possessive_team = 'My'
    else:
        possessive_team = 'Open'

    invite = get_object_or_None(Invite, invitee=u, team=team, status='new')

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
    invite = get_object_or_None(Invite, pk=invite_id, status='new')

    if not invite:
        return

    if action == 'join':
        invite.status = 'accepted'
        invite.accept = datetime.now()
        invite.team.users.add(u)
        messages.success(request, 'Congratulation! Now you are member of %s!' % invite.team.name)

        for i in Invite.objects.filter(invitee=u, status='new').exclude(pk=invite_id).all():
            i.read = datetime.now()
            i.status = 'read'
            i.save()

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
    PERPAGE = 8
    p = request.GET.get('p', 1)
    F = f.FilterForm

    form_data = request.GET.copy()

    if not form_data.get('unit'):
        form_data['unit'] = 'solo'

    if form_data.get('unit') == 'solo' and form_data.get('team_kind'):
        del form_data['team_kind']

    def fish_junior_gender_filter(q):
        junior_dob = date.today() - relativedelta(years=18)
        if filters['age'] == 'junior':
            q = q.filter(user__profile__dob__gt=junior_dob)
        elif filters['age'] == 'open':
            q = q.filter(user__profile__dob__lte=junior_dob)
        return q

    def user_junior_gender_filter(q):
        junior_dob = date.today() - relativedelta(years=18)
        if filters['age'] == 'junior':
            q = q.filter(profile__dob__gt=junior_dob)
        elif filters['age'] == 'open':
            q = q.filter(profile__dob__lte=junior_dob)
        return q

    form = F(form_data or None, request=request)
    if form.is_valid():
        filters = form.cleaned_data

        obj_type = 'user'

        if filters['unit'] == 'solo':
            if filters['species']:
                obj_type = 'fish'
                q = m.Fish.objects \
                    .filter(species=filters['species']) \
                    .order_by('-points')
                q = fish_junior_gender_filter(q)
            elif filters['division']:
                users = User.objects.filter(profile__division=filters['division'])
                q = users.annotate(total_points=Sum('fish__points')).exclude(total_points=0).order_by('-total_points')
                q = user_junior_gender_filter(q)
                q = q.extra(where=['main_fish.species_id != 12'])
            else:
                q = User.objects.annotate(total_points=Sum('fish__points')).exclude(total_points=0).order_by('-total_points')
                q = user_junior_gender_filter(q)
                q = q.extra(where=['main_fish.species_id != 12'])
        else:
            obj_type = 'team'
            teams = Team.objects.annotate(num_users=Count('users', distinct=True)).exclude(num_users__lt=2)
            if filters['division']:
                teams = teams.filter(users__profile__division=filters['division'])
            q = teams.annotate(total_points=Sum('users__fish__points')).exclude(total_points=0).order_by('-total_points')
            q = q.extra(where=['main_fish.species_id != 12'])

        paginator = Paginator(q, PERPAGE)

        page = paginator.page(p)
        start = PERPAGE * (int(p) - 1)

        radios = (form[name] for name in ['unit', 'age'])
        if page.has_next():
            query_params = request.GET.copy()
            query_params['p'] = page.next_page_number()
            query_params_str = query_params.urlencode()
        else:
            query_params_str = None

        return {
            'page': page,
            'start': start,
            'form': form,
            'obj_type': obj_type,
            'radios': radios,
            'next_page_params': query_params_str,
        }
    else:
        print(form.errors)


@login_required
@ajax_request
def ajax_report(request):
    u = request.user
    if request.method == 'POST':
        fish = get_object_or_404(m.Fish, pk=request.POST.get('fish'))

        schema = 'https' if request.is_secure() else 'http'
        base_url = "%s://%s" % (schema, request.get_host())

        page_url = base_url + reverse('fish_enlarge', kwargs={'fish_id': fish.id})

        content = "%s %s reported a page: %s" % (u.first_name, u.last_name, page_url)
        mail_managers('Report', content, fail_silently=False)

        return {'status': 'success'}


def facebook_invite_link(request, team):
    app_id = settings.SOCIAL_AUTH_FACEBOOK_KEY
    schema = 'https' if request.is_secure() else 'http'
    base_url = "%s://%s" % (schema, request.get_host())

    redirect_uri = base_url + reverse('facebook_save_invitee')
    message = "Ocean Hunter Spearfishing Competition 2016/17. Join my team %s!" % team.name

    return "http://www.facebook.com/dialog/apprequests?" \
            "app_id=%(app_id)s" \
            "&message=%(message)s" \
            "&redirect_uri=%(redirect_uri)s" % locals()


def get_admin_access_token(request):
    backend = FacebookOAuth2()

    params = {
        'app_id': settings.SOCIAL_AUTH_FACEBOOK_APP_KEY,
        'scope': 'public_profile,email,manage_pages,publish_pages,publish_actions',
        'next': request.build_absolute_uri(reverse('get_admin_access_token_complete')),
    }
    params = urlencode(params)

    redirect_url = '{0}?{1}'.format(backend.authorization_url(), params)

    return HttpResponseRedirect(redirect_url)


def get_admin_access_token_complete(request):
    code = request.GET['code']

    graph = OpenFacebook()
    params = {
        'code': code,
        'client_id': settings.SOCIAL_AUTH_FACEBOOK_APP_KEY,
        'client_secret': settings.SOCIAL_AUTH_FACEBOOK_SECRET,
        'redirect_uri': request.build_absolute_uri(reverse('get_admin_access_token_complete'))
    }
    resp = graph.get('oauth/access_token', **params)

    FacebookAdminToken.objects.create(access_token=resp['access_token'])
    return HttpResponseRedirect('/admin/')
