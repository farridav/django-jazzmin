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
        # Place before admin
        'adminlteui',

        'django.contrib.admin',
        ...

        # For a custom menu
        'treebeard',
        ...
    ]

Init models
===========

::

    python manage.py migrate django_admin_settings
