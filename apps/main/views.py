from collections import OrderedDict
from datetime import datetime, date
from itertools import chain
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, mail_managers
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Sum, Count
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponseRedirect

from open_facebook import OpenFacebook
from apps.accounts.models import FacebookAdminToken, Team, Invite
from social_core.backends.facebook import FacebookOAuth2

from annoying.functions import get_object_or_None

from dateutil.relativedelta import relativedelta

from apps.main import models as m
from apps.main import forms as f


APP_NAME = 'main'


def T(t, ext='html'):
    return f'{APP_NAME}/{t}.{ext}'

@login_required
def home(request):
    if not request.user.profile.profile_completed:
        return redirect('extra_profile')

    PERPAGE = 8
    EXAMPLE_FISH_ID = 1
    q = m.Fish.objects.exclude(pk=EXAMPLE_FISH_ID).order_by('-create')
    paginator = Paginator(q, PERPAGE)
    p = request.GET.get('p', 1)
    page = paginator.page(p)
    start = PERPAGE * (int(p) - 1)
    feeds = page.object_list
    if int(p) == 1:
        feeds = chain(m.Fish.objects.filter(pk=EXAMPLE_FISH_ID), feeds)

    context = {
        'page': page,
        'start': start,
        'feeds': feeds,
        'TEMPLATE': 'feed.html'
    }
    return render(request, 'home.html', context)


@login_required
def fish_enlarge(request, fish_id):
    context = {
        'enlarge': True,
        'feeds': [get_object_or_404(m.Fish, pk=fish_id)]
    }
    return render(request, 'feed.html', context)


def go(request):
    return render(request, 'go.html')


@login_required
def invite(request):
    if not request.user.profile.profile_completed:
        return redirect('extra_profile')

    u = request.user
    existing_team = get_object_or_None(Team, users=u)
    isadmin = existing_team and existing_team.admin == u
    isfull = existing_team and existing_team.users.count() == 4

    if existing_team and (not isadmin or isfull):
        messages.error(request, 'Sorry, only the admin can invite new members.')
        return redirect('home')

    if date.today() >= date(2017, 2, 1):
        messages.error(request, 'Sorry, you cannot create a team after the 1st of February.')
        return redirect('home')

    context = {'existing_team': existing_team}
    return render(request, 'invite.html', context)


@login_required
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
                return render(request, 'invite_email.html', {'form': form})

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

                subject = f"{u.first_name} {u.last_name} has invited you to join the team {existing_team.name}"
                t = loader.get_template('emails/invitation-inline.html')
                context = {
                    'subject': subject,
                    'user': u,
                    'team': existing_team,
                    'invitation_code': invite.key
                }
                html_content = t.render(context, request)
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

    context = {'form': form, 'existing_team': existing_team}
    return render(request, 'invite_email.html', context)


@login_required
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

    context = {'form': form}
    return render(request, 'invite_facebook.html', context)


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

    context = {'form': form, 'species': species}
    return render(request, 'myfish_new.html', context)


@login_required
def myfish(request, user_id):
    if user_id == 'me' or int(user_id) == request.user.id:
        u = request.user
        possessive = 'My'
        team = get_object_or_None(Team, users=u)
        possessive_team = 'Create' if not team else possessive
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

    context = {
        'u': u,
        'species_list': species_list,
        'possessive': possessive,
        'possessive_team': possessive_team
    }
    return render(request, 'myfish.html', context)


@login_required
def myfish_delete(request):
    u = request.user
    if request.method == 'POST':
        fish_id = request.POST.get('id')
        fish = get_object_or_404(m.Fish, pk=fish_id, user=u)
        fish.delete()
        return redirect('home')


@login_required
def myteam(request, user_id):
    if user_id == 'me' or int(user_id) == request.user.id:
        u = request.user
        possessive = 'My'
    else:
        u = get_object_or_404(User, pk=user_id)
        possessive = 'His' if u.profile.gender == 'male' else 'Her'

    if request.method == 'POST':
        do_team_invite_post(request)

    team = get_object_or_None(Team, users=u)
    possessive_team = 'Create' if possessive == 'My' and not team else possessive

    invite = get_object_or_None(Invite, invitee=request.user, team=team, status='new')

    context = {
        'u': u,
        'possessive': possessive,
        'team': team,
        'invite': invite,
        'possessive_team': possessive_team
    }
    return render(request, 'myfish_myteam.html', context)


@login_required
def team_alone(request, team_id):
    if request.method == 'POST':
        do_team_invite_post(request)

    u = request.user
    team = get_object_or_404(Team, pk=team_id)
    possessive_team = 'My' if request.user in team.users.all() else 'Open'

    invite = get_object_or_None(Invite, invitee=u, team=team, status='new')

    context = {
        'team': team,
        'team_alone': True,
        'invite': invite,
        'possessive_team': possessive_team
    }
    return render(request, 'myfish_myteam.html', context)


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
        messages.success(request, 'Congratulations! You are now a member of %s!' % invite.team.name)

        for i in Invite.objects.filter(invitee=u, status='new').exclude(pk=invite_id).all():
            i.read = datetime.now()
            i.status = 'read'
            i.save()

    elif action == 'reject':
        invite.status = 'read'

    invite.read = datetime.now()
    invite.save()


@login_required
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
                q = m.Fish.objects.filter(species=filters['species']).order_by('-points')
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

        try:
            page = paginator.page(p)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        start = PERPAGE * (int(p) - 1)

        radios = (form[name] for name in ['unit', 'age'])
        next_page_params = None

        if page.has_next():
            query_params = request.GET.copy()
            query_params['p'] = page.next_page_number()
            next_page_params = query_params.urlencode()

        context = {
            'page': page,
            'start': start,
            'form': form,
            'obj_type': obj_type,
            'radios': radios,
            'next_page_params': next_page_params
        }
        return render(request, 'leaderboard.html', context)
    else:
        print(form.errors)
        return render(request, 'leaderboard.html', {'form': form})


@login_required
def ajax_report(request):
    u = request.user
    if request.method == 'POST':
        fish = get_object_or_404(m.Fish, pk=request.POST.get('fish'))

        schema = 'https' if request.is_secure() else 'http'
        base_url = f"{schema}://{request.get_host()}"

        page_url = base_url + reverse('fish_enlarge', kwargs={'fish_id': fish.id})

        content = f"{u.first_name} {u.last_name} reported a page: {page_url}"
        mail_managers('Report', content, fail_silently=False)

        return {'status': 'success'}


def facebook_invite_link(request, team):
    app_id = settings.SOCIAL_AUTH_FACEBOOK_KEY
    schema = 'https' if request.is_secure() else 'http'
    base_url = f"{schema}://{request.get_host()}"

    redirect_uri = base_url + reverse('facebook_save_invitee')
    message = f"Ocean Hunter Spearfishing Competition 2016/17. Join my team {team.name}!"

    return f"http://www.facebook.com/dialog/apprequests?app_id={app_id}&message={message}&redirect_uri={redirect_uri}"


def get_admin_access_token(request):
    backend = FacebookOAuth2()

    params = {
        'app_id': settings.SOCIAL_AUTH_FACEBOOK_APP_KEY,
        'scope': 'public_profile,email,manage_pages,publish_pages,publish_actions',
        'next': request.build_absolute_uri(reverse('get_admin_access_token_complete')),
    }
    params = urlencode(params)

    redirect_url = f'{backend.authorization_url()}?{params}'

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
