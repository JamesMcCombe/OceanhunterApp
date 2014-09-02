#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
from fabric.api import *
from path import path
from os.path import dirname,abspath
HERE = path(dirname(abspath(__file__)))
PROJ_NAME = HERE.parent.name
WORKON_HOME = path('/var/www/django')
VENV_ROOT = WORKON_HOME/PROJ_NAME
PROJ_ROOT = VENV_ROOT/PROJ_NAME
ACTIVATE = VENV_ROOT/'bin'/'activate'

env.use_ssh_config = True
env.hosts = ['nodedev']
env.activate = 'source %s' % ACTIVATE
env.deploy_dir = PROJ_ROOT
from contextlib import contextmanager

@contextmanager
def virtualenv():
    with prefix(env.activate):
        yield


def coffee():
    pass


def pull():
    local('git push')
    with cd(env.deploy_dir):
        run("git pull")

def static():
    with cd(env.deploy_dir):
        coffee()
        run("sass static/sass/main.scss:static/css/main.css --style compressed")
        with virtualenv():
            run('python manage.py collectstatic --noinput')

def touch():
    with cd(env.deploy_dir):
        run("touch *.ini")

def all():
    pull()
    static()
