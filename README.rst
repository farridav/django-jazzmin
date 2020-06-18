Django jazzmin (Jazzy Admin)
============================

.. image:: https://readthedocs.org/projects/django-jazzmin/badge/?version=latest
   :target: http://django-jazzmin.readthedocs.io/?badge=latest
.. image:: https://img.shields.io/pypi/dm/django-jazzmin.svg
.. image:: https://badge.fury.io/py/django-jazzmin.svg
   :target: https://pypi.python.org/pypi/django-jazzmin/
.. image:: https://img.shields.io/pypi/pyversions/django-jazzmin.svg
.. image:: https://img.shields.io/pypi/djversions/django-jazzmin.svg
.. image:: https://coveralls.io/repos/github/farridav/django-jazzmin/badge.svg?branch=master
   :target: https://coveralls.io/github/farridav/django-jazzmin?branch=master

Drop-in theme for django admin, that utilises AdminLTE 3 & Bootstrap 4 to make yo' admin look jazzy

Documentation
-------------
See https://django-jazzmin.readthedocs.io also see `Test App`_

Demo
----
Live demo https://django-jazzmin.herokuapp.com/admin

**Username**: test@test.com

**Password**: test

*Note: Data resets nightly*

Features
--------
- Drop-in admin skin, all configuration optional
- Select2 drop-downs
- Bootstrap 4 & AdminLTE UI components
- Customisable `side menu`_
- Customisable `top menu`_
- Customisable `user menu`_
- Search bar for any given model admin
- Customisable UI (via `Live UI changes`_, or `custom CSS/JS`_)
- Responsive
- Based on the latest `adminlte`_ + `bootstrap`_

Screenshots
-----------

Dashboard
~~~~~~~~~
.. image:: https://django-jazzmin.readthedocs.io/img/dashboard.png

List view
~~~~~~~~~
.. image:: https://django-jazzmin.readthedocs.io/img/list_view.png

Detail view
~~~~~~~~~~~
.. image:: https://django-jazzmin.readthedocs.io/img/detail_view.png

History page
~~~~~~~~~~~~
.. image:: https://django-jazzmin.readthedocs.io/img/history_page.png

Login view
~~~~~~~~~~
.. image:: https://django-jazzmin.readthedocs.io/img/login.png

UI Customiser
~~~~~~~~~~~~~
.. image:: https://django-jazzmin.readthedocs.io/img/ui_customiser.png

Mobile layout
~~~~~~~~~~~~~
.. image:: https://django-jazzmin.readthedocs.io/img/dashboard_mobile.png

Tablet layout
~~~~~~~~~~~~~
.. image:: https://django-jazzmin.readthedocs.io/img/dashboard_tablet.png

Admin Docs (if installed)
~~~~~~~~~~~~~~~~~~~~~~~~~
.. image:: https://django-jazzmin.readthedocs.io/img/admin_docs.png

.. _adminlte: https://adminlte.io/
.. _bootstrap: https://getbootstrap.com
.. _Test App: https://github.com/farridav/django-jazzmin/tree/master/tests/test_app
.. _top menu: https://github.com/farridav/django-jazzmin/blob/master/tests/test_app/settings.py#L62
.. _side menu: https://github.com/farridav/django-jazzmin/blob/master/tests/test_app/settings.py#L92
.. _user menu: https://github.com/farridav/django-jazzmin/blob/master/tests/test_app/settings.py#L86
.. _Live UI changes: https://github.com/farridav/django-jazzmin/blob/master/tests/test_app/settings.py#L133
.. _custom CSS/JS: https://github.com/farridav/django-jazzmin/blob/master/tests/test_app/settings.py#L129
