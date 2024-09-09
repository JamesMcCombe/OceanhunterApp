from os.path import abspath, dirname
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from annoying.decorators import render_to, ajax_request
from django.contrib import messages
from annoying.functions import get_object_or_None
from apps.accounts.models import Invite
from apps.accounts import forms as f
from apps.pages.models import Page


APP_NAME = __name__.split('.')[0]


def T(name, ext='html'):
    return f'{APP_NAME}/{name}.{ext}'


def signup(request):
    F = f.SignupForm
    if request.method == 'GET':
        form = F(request=request)
    else:
        form = F(data=request.POST, request=request)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email=email, password=password)
            auth_login(request, user)
            for invite in Invite.objects.filter(via='email', ref=email):
                invite.invitee = user
                invite.save()
            return redirect('invite')
        else:
            print("Form is not valid")
            print(form.errors)
    rules = get_object_or_None(Page, slug='rules-conditions')
    ctx = {'form': form, 'rules': rules}
    return render(request, T('signup'), ctx)


@render_to(T('login'))
def login(request):
    F = f.LoginForm
    if request.method == 'GET':
        form = F()
    else:
        form = F(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user and user.is_active:
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect(request.POST.get('next', 'home'))
            else:
                messages.error(request, 'The username and password were incorrect.')
    ctx = {'form': form}
    ctx['public'] = 'public'
    ctx['next'] = request.GET.get('next', 'home')
    return ctx


@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')


@login_required
@render_to(T('extra_profile'))
def extra_profile(request):
    u = request.user
    F = f.ExtraProfileForm
    if request.method == 'GET':
        form = F(instance=u.profile)
    else:
        form = F(data=request.POST, instance=u.profile)
        if form.is_valid():
            form.save()
            return redirect('invite')
    rules = get_object_or_None(Page, slug='rules-conditions')
    ctx = {'form': form, 'rules': rules}
    return ctx


@ajax_request
def fbuser(request):
    data = request.GET
    if not data:
        return {'ret': False, 'msg': 'No GET Data'}
    username = data.get('id')
    if not username:
        return {'ret': False, 'msg': 'No id'}
    password = '!'
    u, _ = User.objects.get_or_create(username=username)
    u.set_password(password)
    u.first_name = data.get('first_name')
    u.last_name = data.get('last_name')
    u.name = data.get('name')
    u.gender = data.get('gender')
    u.link = data.get('link')
    u.locale = data.get('locale')
    u.timezone = data.get('timezone')
    u.verified = data.get('verified')
    u.save()
    u = authenticate(username=username, password=password)
    if u is not None and u.is_active:
        auth_login(request, u)
    return {'ret': True, 'msg': 'ok!'}
