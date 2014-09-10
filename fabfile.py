#!/usr/bin/env python
# encoding: utf-8
from fabric.api import *
env.use_ssh_config = True
env.hosts = ['nodeweb']
env.activate = 'source /var/www/django/oceanhunter/bin/activate'
env.deploy_dir = '/var/www/django/oceanhunter/oceanhunter'
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
        run("sass static/scss/main.scss:static/build/css/main.css --style compressed")
        with virtualenv():
            run('python manage.py collectstatic --noinput')

def touch():
    with cd(env.deploy_dir):
        run("touch *.ini")

def all():
    pull()
    static()
