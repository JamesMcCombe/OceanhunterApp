from path import path
from os.path import abspath,dirname
from django.shortcuts import redirect
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login  as auth_login
from django.contrib.auth import logout as auth_logout
from annoying.decorators import render_to
#from . import models as m
from . import forms  as f

APP_ROOT = path(dirname(abspath(__file__)))
APP_NAME = APP_ROOT.name

def T(name, ext='html'):
    return '{}/{}.{}'.format(APP_NAME, name, ext)

@render_to(T('signup'))
def signup(request):
    F = f.SignupForm
    if request.method == 'GET':
        form = F()
    else:
        form = F(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    ctx = {'form': form}
    return ctx


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
                auth_login(request,user)
                return redirect('home')
    ctx = {'form': form}
    ctx['public'] = 'public'
    return ctx


@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')
