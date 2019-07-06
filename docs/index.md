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
    # custom menu base on treebeard
    'treebeard',
    ...
]
```

## Init models
```
python manage.py migrate django_admin_settings
```
## screen shot

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

## Thanks

- [AdminLTE](https://github.com/ColorlibHQ/AdminLTE)
- [django](https://github.com/django/django)
- [django-treebeard](https://github.com/django-treebeard/django-treebeard)
- [django-suit](https://github.com/darklow/django-suit)
