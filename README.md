## About
A great, flat, reuseable, portable django layout template project.
This is intended for single sites only if you want multi site support please use the default layout.

## Quickstart
Make you have virtualenv and virtualenvwrapper installed.

```bash
mkvirtualenv ENV
```

First, clone the project to your machine:

```bash
git clone git@bitbucket.org:nodedigital/django-layout.git
```

Then, use this layout as a template to start your project:

```bash
django-admin.py startproject --template=django-layout PROJECT_NAME
```

# CMS Support
***install django < 1.6***

```bash
pip install django==1.5.5
```

***change branch to CMS***
```bash
git pull --all
git checkout cms
```

