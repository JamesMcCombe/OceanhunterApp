# #!/usr/bin/env python
# # encoding: utf-8
# from fabric.api import *
# from path import path
# from os.path import dirname,abspath
# HERE = path(dirname(abspath(__file__)))
# PROJ_NAME = HERE.name
# WORKON_HOME = path('/var/www/django')
# VENV_ROOT = WORKON_HOME/PROJ_NAME
# PROJ_ROOT = VENV_ROOT/PROJ_NAME
# BIN = VENV_ROOT/'bin'
# ACTIVATE = BIN/'activate'


# # ilian's settings
# from unipath import Path
# APPLICATIONS_DIR = '/var/apps'
# VIRTUALENVWRAPPER_SCRIPT = 'source /usr/local/bin/virtualenvwrapper.sh'


# PROJ_ROOT = Path(APPLICATIONS_DIR, PROJ_NAME)





# env.use_ssh_config = True
# # env.hosts = ['nodeweb']
# PROJ_NAME = 'oceanhunter'
# env.activate = 'source %s' % ACTIVATE
# env.deploy_dir = PROJ_ROOT
# from contextlib import contextmanager

# @contextmanager
# def virtualenv():
#     with prefix(env.activate):
#         yield


# def pull():
#     local('git push')
#     with cd(env.deploy_dir):
#         run("git pull")

# def static():
#     with cd(env.deploy_dir):
#         with cd('static'):
#             run('mkdir -p build/js build/css')
#             run('gulp sass coffee')
#         with virtualenv():
#             run('python manage.py collectstatic --noinput -i node_modules')

# def touch():
#     with cd(env.deploy_dir):
#         run("touch deploy/*.ini")
#     tail()

# def tail():
#     run("tail -f /var/log/uwsgi/%s.log" % PROJ_NAME)

# def all():
#     pull()
#     static()
#     touch()


# def deploy():
#     with cd(env.deploy_dir):
#         run("git pull")
#         run("touch deploy/*.ini")

#         with prefix(VIRTUALENVWRAPPER_SCRIPT):
#             with prefix('workon {0}'.format(PROJ_NAME)):
#                 run('python manage.py collectstatic --noinput -i node_modules')
