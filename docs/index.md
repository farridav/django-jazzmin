# Welcome to django-adminlte-ui

[![PyPI Version](https://img.shields.io/pypi/v/django-adminlte-ui.svg)](https://pypi.python.org/pypi/django-adminlte-ui)
[![Download Status](https://img.shields.io/pypi/dm/django-adminlte-ui.svg)](https://pypi.python.org/pypi/django-adminlte-ui)
[![Build Status](https://api.travis-ci.org/wuyue92tree/django-adminlte-ui.svg)](https://travis-ci.org/wuyue92tree/django-adminlte-ui)

django-adminlte is a django admin theme base on adminlte

adminlte version: 2.3.6


## Helper

- if you have good ideas, just contact me.
- if you find some bug, just add an issue.
- if you think this project is good, just star and fork, make it better 🍉.


## Install

```
pip install django-adminlte-ui
```

## Setup

```
# settings.py

INSTALLED_APPS = [
    'adminlteui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ...
]
```

## Init models
```
python manage.py migrate django_admin_settings
```

## Guides

### General Option

dynamic setup your site base on table `django_admin_settings_options`.

support options:

- Site Title
- Site Header
- Site Logo
- Welcome Sign

### Options

this options in your db, named `django_admin_settings_options`, after do migrate.

you can also add your custom option into this table, and use it by templatetags
 `adminlte_options` with function `get_adminlte_option`.

options table has a valid field to control your option work or not.


example:

```
# adminlte/general_option.html

{% load adminlte_options %}

# here my option_name is site_title, you can custom yourself.
{% get_adminlte_option 'site_title' as adminlte_site_title %}
{% if adminlte_site_title.valid %}
{{ adminlte_site_title.site_title }}
{% else %}
{{ site_title|default:_('Django site admin') }}
{% endif %}

```

before custom option, you should known what adminlte has used.

- site_title
- site_header
- site_logo
- welcome_sign


### Menu

coming soon...
