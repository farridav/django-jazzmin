# Django jazzmin (Jazzy Admin)

[![Docs](https://readthedocs.org/projects/django-jazzmin/badge/?version=latest)](http://django-jazzmin.readthedocs.io/?badge=latest)
![PyPI download month](https://img.shields.io/pypi/dm/django-jazzmin.svg)
[![PyPI version](https://badge.fury.io/py/django-jazzmin.svg)](https://pypi.python.org/pypi/django-jazzmin/)
![Python versions](https://img.shields.io/pypi/pyversions/django-jazzmin.svg)
![Django Versions](https://img.shields.io/pypi/djversions/django-jazzmin.svg)
[![Coverage Status](https://coveralls.io/repos/github/farridav/django-jazzmin/badge.svg?branch=master)](https://coveralls.io/github/farridav/django-jazzmin?branch=master)

Drop-in theme for django admin, that utilises AdminLTE 3 & Bootstrap 4 to make yo' admin look jazzy

## Installation
```
pip install django-jazzmin
```

## Documentation
See [Documentation](https://django-jazzmin.readthedocs.io/) or [Test App](./tests/test_app/settings.py)

## Demo
Live demo https://django-jazzmin.herokuapp.com/admin

**Username**: test@test.com

**Password**: test

*Note: Data resets nightly*

## Features
- Drop-in admin skin, all configuration optional
- Customisable side menu
- Customisable top menu
- Customisable user menu
- Customisable UI (via Live UI changes, or custom CSS/JS)
- Based on the latest [adminlte](https://adminlte.io/) + [bootstrap](https://getbootstrap.com/)

## Screenshots

## Dashboard
![dashboard](docs/img/dashboard.png)

## List view
![table list](docs/img/list_view.png)

## Detail view
![form page](docs/img/detail_view.png)

## History page
![form page](docs/img/history_page.png)

## Login view
![login](docs/img/login.png)

## UI Customiser
![ui_customiser](docs/img/ui_customiser.png)

## Mobile layout
![mobile](docs/img/dashboard_mobile.png)

## Tablet layout
![tablet](docs/img/dashboard_tablet.png)

## Admin Docs (if installed)
![admin_docs](docs/img/admin_docs.png)

## Thanks
This was initially a Fork of https://github.com/wuyue92tree/django-adminlte-ui that we refactored so much we thought it
deserved its own package, big thanks to @wuyue92tree for all of his initial hard work, we are still patching into that
project were possible, but this project is taking a slightly different direction.

- Based on AdminLTE 3: https://adminlte.io/
- Using Bootstrap 4: https://getbootstrap.com/
- Using Font Awesome 5: https://fontawesome.com/
