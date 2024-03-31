
# Django jazzmin (Jazzy Admin)

## Project Status

This project is being actively maintained, though with a reduced feature set, we are looking for contributors to help
maintain and improve the project, please get in touch if you would like to help.

Help needed with:

- Triaging issues
- Frontend fixes and UI improvements
- Testing
- Documentation

Pull requests are welcome, though ive been pre-occupied with other projects lately, so have not been able to review
them as quickly as I would like, but im trying to get through them all now, hopefully with some outside help.

[![Docs](https://readthedocs.org/projects/django-jazzmin/badge/?version=latest)](https://django-jazzmin.readthedocs.io)
![PyPI download month](https://img.shields.io/pypi/dm/django-jazzmin.svg)
[![PyPI version](https://badge.fury.io/py/django-jazzmin.svg)](https://pypi.python.org/pypi/django-jazzmin/)
![Python versions](https://img.shields.io/badge/python-%3E=3.8-brightgreen)
![Django Versions](https://img.shields.io/badge/django-%3E=4.2-brightgreen)
[![Coverage Status](https://coveralls.io/repos/github/farridav/django-jazzmin/badge.svg?branch=master)](https://coveralls.io/github/farridav/django-jazzmin?branch=master)

Drop-in theme for django admin, that utilises AdminLTE 3 & Bootstrap 4 to make yo' admin look jazzy

## Installation

```bash
pip install django-jazzmin
```

## Documentation

See [Documentation](https://django-jazzmin.readthedocs.io) or [Test App](https://github.com/farridav/django-jazzmin/tree/master/tests/test_app/library/settings.py)

## Features

- Drop-in admin skin, all configuration optional
- Customisable side menu
- Customisable top menu
- Customisable user menu
- 4 different Change form templates (horizontal tabs, vertical tabs, carousel, collapsible)
- Bootstrap 4 modal (instead of the old popup window, optional)
- Search bar for any given model admin
- Customisable UI (via Live UI changes, or custom CSS/JS)
- Responsive
- Select2 drop-downs
- Bootstrap 4 & AdminLTE UI components
- Using the latest [adminlte](https://adminlte.io/) + [bootstrap](https://getbootstrap.com/)

## Screenshots

## Dashboard

![dashboard](https://django-jazzmin.readthedocs.io/img/dashboard.png)

## List view

![table list](https://django-jazzmin.readthedocs.io/img/list_view.png)

## Change form templates

### Collapsed side menu

![form page](https://django-jazzmin.readthedocs.io/img/detail_view.png)

### Expanded side menu

![Single](https://django-jazzmin.readthedocs.io/img/changeform_single.png)

### Horizontal tabs

![Horizontal tabs](https://django-jazzmin.readthedocs.io/img/changeform_horizontal_tabs.png)

### Vertical tabs

![Vertical tabs](https://django-jazzmin.readthedocs.io/img/changeform_vertical_tabs.png)

### Collapsible

![Collapsible](https://django-jazzmin.readthedocs.io/img/changeform_collapsible.png)

### Carousel

![Carousel](https://django-jazzmin.readthedocs.io/img/changeform_carousel.png)

### Related modal

![Related modal](https://django-jazzmin.readthedocs.io/img/related_modal_bootstrap.png)

## History page

![form page](https://django-jazzmin.readthedocs.io/img/history_page.png)

## Login view

![login](https://django-jazzmin.readthedocs.io/img/login.png)

## UI Customiser

![ui_customiser](https://django-jazzmin.readthedocs.io/img/ui_customiser.png)

## Mobile layout

![mobile](https://django-jazzmin.readthedocs.io/img/dashboard_mobile.png)

## Tablet layout

![tablet](https://django-jazzmin.readthedocs.io/img/dashboard_tablet.png)

## Admin Docs (if installed)

![admin_docs](https://django-jazzmin.readthedocs.io/img/admin_docs.png)

## Thanks

This was initially a Fork of <https://github.com/wuyue92tree/django-adminlte-ui> that we refactored so much we thought it
deserved its own package, big thanks to @wuyue92tree for all of his initial hard work, we are still patching into that
project were possible, but this project has taken a different direction.

The javascript modal implementation uses some code from [django-admin-interface](https://github.com/fabiocaccamo/django-admin-interface/blob/master/admin_interface/static/admin/js/popup_response.js), so thanks to @fabiocaccamo for original work

- Based on AdminLTE 3: <https://adminlte.io/>
- Using Bootstrap 4: <https://getbootstrap.com/>
- Using Font Awesome 5: <https://fontawesome.com/>
