from collections import OrderedDict
from datetime import datetime, date
from itertools import chain

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, mail_managers
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.db.models import Sum, Case, When, DecimalField
from django.http import HttpResponseRedirect

from apps.accounts.models import Team, Invite
from apps.main import models as m
from apps.main import forms as f

from annoying.functions import get_object_or_None


def get_facebook_page_token(access_token):
    """Get the Facebook Page Token using the given access token."""
    url = 'https://graph.facebook.com/me/accounts'
    params = {'access_token': access_token}
    response = requests.get(url, params=params)
    return response.json()


def post_to_facebook(page_token, message, img_url, link_url):
    """Post to Facebook using the Page Token."""
    url = 'https://graph.facebook.com/me/feed'
    params = {
        'access_token': page_token,
        'message': message,
        'link': link_url,
        'picture': img_url
    }
    response = requests.post(url, data=params)
    return response.json()


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

    if p == 1:
        feeds = chain(m.Fish.objects.filter(pk=EXAMPLE_FISH_ID), feeds)

    context = {
        'page': page,
        'start': start,
        'feeds': feeds,
        'TEMPLATE': 'feed.html',
    }
    return render(request, 'home.html', context)


@login_required
def fish_enlarge(request, fish_id):
    fish = get_object_or_404(m.Fish, pk=fish_id)
    context = {
        'enlarge': True,
        'feeds': [fish],
    }
    return render(request, 'feed.html', context)


def go(request):
    return render(request, 'go.html')


@login_required
def invite(request):
    u = request.user
    existing_team = get_object_or_None(Team, users=u)
    isadmin = existing_team and existing_team.admin == u
    isfull = existing_team and existing_team.users.count() == 4

    if existing_team and (not isadmin or isfull):
        messages.error(request, 'Sorry, only the admin can invite new members.')
        return redirect('home')

    context = {'existing_team': existing_team}
    return render(request, 'invite.html', context)


@login_required
def invite_email(request):
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
                messages.error(request, f'You cannot invite {email} who already has a team.')
                continue
            success_invitations.append(email)
            data = dict(inviter=u, team=existing_team, via='email', ref=email, status='new')
            invite = get_object_or_None(Invite, **data) or Invite(**data)
            invite.save()

            if email_user:
                invite.invitee = email_user
                invite.save()

            subject = f"{u.first_name} {u.last_name} has invited you to join the team {existing_team.name}"
            t = loader.get_template('emails/invitation-inline.html')
            html_content = t.render({'subject': subject, 'user': u, 'team': existing_team})
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

    return render(request, 'invite_email.html', {'form': form, 'existing_team': existing_team})


@login_required
def invite_facebook(request):
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
    return render(request, 'invite_facebook.html', {'form': form})


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
        invite = get_object_or_None(Invite, **data) or Invite(**data)
        invite.save()

        if fb_user:
            invite.invitee = fb_user
            invite.save()

    messages.success(request, 'Invites have been sent.')
    if u.profile.is_new():
        return redirect('myfish_new')
    else:
        return redirect('invite')


@login_required
def myfish_new(request):
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
    u = request.user if user_id == 'me' or int(user_id) == request.user.id else get_object_or_404(User, pk=user_id)
    possessive = 'My' if u == request.user else 'Their'
    possessive_team = 'Create' if not get_object_or_None(Team, users=u) else possessive

    species_list = OrderedDict()
    for fish in u.fish_set.order_by('-points'):
        species_list.setdefault(fish.species, [])
        species_list[fish.species].append(fish)

    for species, fishes in species_list.items():
        species.points = sum(f.points for f in fishes)
        species.weight = sum(f.weight for f in fishes)

    context = {'u': u, 'species_list': species_list, 'possessive': possessive, 'possessive_team': possessive_team}
    return render(request, 'myfish.html', context)


@login_required
def myfish_delete(request):
    if request.method == 'POST':
        fish_id = request.POST.get('id')
        fish = get_object_or_404(m.Fish, pk=fish_id, user=request.user)
        fish.delete()
        return redirect('home')


@login_required
def myteam(request, user_id):
    u = request.user if user_id == 'me' or int(user_id) == request.user.id else get_object_or_404(User, pk=user_id)
    possessive = 'My' if u == request.user else 'Their'

    if request.method == 'POST':
        do_team_invite_post(request)

    team = get_object_or_None(Team, users=u)
    possessive_team = possessive if possessive == 'My' and team else 'Create'

    invite = get_object_or_None(Invite, invitee=request.user, team=team, status='new')

    context = {'u': u, 'possessive': possessive, 'team': team, 'invite': invite, 'possessive_team': possessive_team}
    return render(request, 'myfish_myteam.html', context)


@login_required
def team_alone(request, team_id):
    if request.method == 'POST':
        do_team_invite_post(request)

    team = get_object_or_404(Team, pk=team_id)
    possessive_team = 'My' if request.user in team.users.all() else 'Open'

    invite = get_object_or_None(Invite, invitee=request.user, team=team, status='new')

    context = {'team': team, 'team_alone': True, 'invite': invite, 'possessive_team': possessive_team}
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
        invite.team.recalculate_points()
        messages.success(request, f'Congratulations! You are now a member of {invite.team.name}.')

        Invite.objects.filter(invitee=u, status='new').exclude(pk=invite_id).update(status='read', read=datetime.now())

    elif action == 'reject':
        invite.status = 'read'

    invite.read = datetime.now()
    invite.save()


@login_required
def ajax_new_comment(request):
    if request.method == 'POST':
        form = f.CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return {'status': 'success'}
        else:
            return {'status': 'error', 'errors': form.errors}


def leaderboard(request):
    PERPAGE = 8
    p = request.GET.get('p', 1)
    F = f.FilterForm

    form_data = request.GET.copy()
    if not form_data.get('type'):
        form_data['type'] = 'total'

    form = F(form_data or None, request=request)
    if form.is_valid():
        filters = form.cleaned_data
        obj_type = 'user'

        if filters.get('type') == 'total':
            users = User.objects.annotate(total_points=Sum(Case(
                When(fish__status='normal', then='fish__points'),
                default=0,
                output_field=DecimalField(max_digits=10, decimal_places=3)
            ))).exclude(total_points=0).order_by('-total_points')

            if filters['division']:
                users = users.filter(profile__division=filters['division'])

            q = users
        else:
            obj_type = 'fish'
            q = m.Fish.objects.filter(status='normal').order_by('-points')
            if filters['division']:
                q = q.filter(user__profile__division=filters['division'])

        paginator = Paginator(q, PERPAGE)
        page = paginator.page(p)
        start = PERPAGE * (int(p) - 1)

        radios = (form[name] for name in ['type'])
        context = {
            'page': page,
            'start': start,
            'form': form,
            'obj_type': obj_type,
            'radios': radios,
            'next_page_params': request.GET.copy().urlencode() if page.has_next() else None,
        }
        return render(request, 'leaderboard.html', context)
    else:
        return render(request, 'leaderboard.html', {'form': form})


@login_required
def ajax_report(request):
    if request.method == 'POST':
        fish = get_object_or_404(m.Fish, pk=request.POST.get('fish'))

        base_url = f"{'https' if request.is_secure() else 'http'}://{request.get_host()}"
        page_url = base_url + reverse('fish_enlarge', kwargs={'fish_id': fish.id})

        content = f"{request.user.first_name} {request.user.last_name} reported a page: {page_url}"
        mail_managers('Report', content, fail_silently=False)

        return {'status': 'success'}


def facebook_invite_link(request, team):
    app_id = settings.SOCIAL_AUTH_FACEBOOK_KEY
    base_url = f"{'https' if request.is_secure() else 'http'}://{request.get_host()}"
    redirect_uri = base_url + reverse('facebook_save_invitee')
    message = f"Ocean Hunter Spearfishing Competition. Join my team {team.name}!"

    return f"http://www.facebook.com/dialog/apprequests?app_id={app_id}&message={message}&redirect_uri={redirect_uri}"


def get_admin_access_token(request):
    backend = 'social_core.backends.facebook.FacebookOAuth2'
    params = {
        'app_id': settings.SOCIAL_AUTH_FACEBOOK_APP_KEY,
        'scope': 'public_profile,email,manage_pages,publish_pages',
        'next': request.build_absolute_uri(reverse('get_admin_access_token_complete')),
    }

    redirect_url = f"https://www.facebook.com/v3.3/dialog/oauth?client_id={params['app_id']}&redirect_uri={params['next']}&scope={params['scope']}"
    return HttpResponseRedirect(redirect_url)


def get_admin_access_token_complete(request):
    code = request.GET['code']
    params = {
        'client_id': settings.SOCIAL_AUTH_FACEBOOK_APP_KEY,
        'client_secret': settings.SOCIAL_AUTH_FACEBOOK_SECRET,
        'redirect_uri': request.build_absolute_uri(reverse('get_admin_access_token_complete')),
        'code': code
    }

    response = requests.get('https://graph.facebook.com/v3.3/oauth/access_token', params=params)
    access_token = response.json().get('access_token')

    # Save the access token (You need to handle storage securely)
    # Example: FacebookAdminToken.objects.create(access_token=access_token)
    
    return HttpResponseRedirect('/admin/')
