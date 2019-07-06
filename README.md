<p align="center">
  <a href="https://github.com/wuyue92tree/django-adminlte-ui">
    <img alt="title" src="./images/django-adminlte-ui.jpg" width="400">
  </a>
</p>

# django-adminlte-ui
[![PyPI Version](https://img.shields.io/pypi/v/django-adminlte-ui.svg)](https://pypi.python.org/pypi/django-adminlte-ui)
[![Download Status](https://img.shields.io/pypi/dm/django-adminlte-ui.svg)](https://pypi.python.org/pypi/django-adminlte-ui)
[![Build Status](https://api.travis-ci.org/wuyue92tree/django-adminlte-ui.svg)](https://travis-ci.org/wuyue92tree/django-adminlte-ui)
[![Documentation Status](https://readthedocs.org/projects/django-adminlte-ui/badge/?version=latest)](https://django-adminlte-ui.readthedocs.io/en/latest/?badge=latest)

django admin theme base on adminlte

adminlte version: 2.3.6

# helper

- if you have good ideas, just contact me.
- if you find some bug, just add an issue.
- if you think this project is good, just star and fork, make it better 🍉.

# install

```
pip install django-adminlte-ui
```

# setup

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

# Init models
```
python manage.py migrate django_admin_settings
```

# screen shot

## login page
![login](./images/login.jpg)

## dashboard
![dashboard](./images/dashboard.jpg)

## table list
![table list](./images/table-list.jpg)

## form page
![form page](./images/form.png)

## general_option
![general_option](./images/general_option.jpg)

# Thanks

- [AdminLTE](https://github.com/ColorlibHQ/AdminLTE)
- [django](https://github.com/django/django)
- [django-treebeard](https://github.com/django-treebeard/django-treebeard)
- [django-suit](https://github.com/darklow/django-suit)

# Donate

Your donation take me higher. 🚀

<p align="left">
  <a href="https://github.com/wuyue92tree/django-adminlte-ui">
    <img alt="title" src="./images/alipay.png" width="200px">
  </a>
</p>
