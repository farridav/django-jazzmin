django-adminlte-ui
==================

django admin theme base on adminlte

adminlte version: 2.3.6

install
=======

::

    pip install django-adminlte-ui

setup
=====

::

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

Init models
===========

::

    python manage.py migrate django_admin_settings
