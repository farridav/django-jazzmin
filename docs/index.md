# Welcome to django-adminlte-ui

[![PyPI Version](https://img.shields.io/pypi/v/django-adminlte-ui.svg)](https://pypi.python.org/pypi/django-adminlte-ui)
[![Download Status](https://img.shields.io/pypi/dm/django-adminlte-ui.svg)](https://pypi.python.org/pypi/django-adminlte-ui)
[![Build Status](https://api.travis-ci.org/wuyue92tree/django-adminlte-ui.svg)](https://travis-ci.org/wuyue92tree/django-adminlte-ui)
[![Gitter](https://badges.gitter.im/django-adminlte-ui/community.svg)](https://gitter.im/django-adminlte-ui/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)


django-adminlte is a django admin theme base on adminlte

adminlte version: 2.3.6


## Helper

- if you have good ideas, just contact me.
- if you find some bug, just add an issue.
- if you think this project is good, just star and fork, make it better 🍉.

## Demo

[Chinese](http://django-demo.antio.top/zh-hans/admin/)

[English](http://django-demo.antio.top/en/admin/)

- username: demo
- password: demo123
 
database will restore every hour. 🍌


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
    # custom menu base on treebeard
    'treebeard',
    ...
]
```

## Init models
```
python manage.py migrate django_admin_settings
```
## Screen shot

### login page
![login](https://github.com/wuyue92tree/django-adminlte-ui/blob/master/images/login.jpg?raw=true)

### dashboard
![dashboard](https://github.com/wuyue92tree/django-adminlte-ui/blob/master/images/dashboard.jpg?raw=true)

### table list
![table list](https://github.com/wuyue92tree/django-adminlte-ui/blob/master/images/table-list.jpg?raw=true)

### form page
![form page](https://github.com/wuyue92tree/django-adminlte-ui/blob/master/images/form.png?raw=true)

### general_option
![general_option](https://github.com/wuyue92tree/django-adminlte-ui/blob/master/images/general_option.jpg?raw=true)

### menu list
![menu list](https://github.com/wuyue92tree/django-adminlte-ui/blob/master/images/menu-list.png?raw=true)


## Features

- [Custom General Option](https://django-adminlte-ui.readthedocs.io/en/latest/guide/#general-option)
- [Widgets](https://django-adminlte-ui.readthedocs.io/en/latest/guide/#widgets)
- [Custom Menu](https://django-adminlte-ui.readthedocs.io/en/latest/guide/#menu)

## Todo

- Custom Dashboard


## Thanks

- [AdminLTE](https://github.com/ColorlibHQ/AdminLTE)
- [django](https://github.com/django/django)
- [django-treebeard](https://github.com/django-treebeard/django-treebeard)
- [django-suit](https://github.com/darklow/django-suit)
