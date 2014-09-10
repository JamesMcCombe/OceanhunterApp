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


def pull():
    local('git push')
    with cd(env.deploy_dir):
        run("git pull")

def static():
    with cd(env.deploy_dir):
        with cd('static'):
            run('mkdir -p build/js build/css')
            run('gulp sass coffee')
        with virtualenv():
            run('python manage.py collectstatic --noinput -i node_modules')

def touch():
    with cd(env.deploy_dir):
        run("touch deploy/*.ini")

def all():
    pull()
    static()
