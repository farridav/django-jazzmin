# Jazzmin

## Installation

Install the latest [pypi](https://pypi.org/project/django-jazzmin/) release with `pip install -U django-jazzmin`

Add `jazzmin` to your `INSTALLED_APPS` before `django.contrib.admin`, and voila!

```python
INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    [...]
]
```

## Features

- Drop-in, configure only if you want to
- Customisable side menu
- Customisable top menu
- Customisable UI (via Live UI changes, or custom CSS/JS)
- Based on the latest [adminlte](https://adminlte.io/) + [bootstrap](https://getbootstrap.com/)

See [configuration](./configuration.md) for optional customisation of the theme

See [development](./development.md) for notes on setting up for development

## Screenshots

### Dashboard
![dashboard](./img/dashboard.png)

### List view
![table list](./img/list_view.png)

### Detail view
![form page](./img/detail_view.png)

### Login view
![login](./img/login.png)

### UI Customiser
![login](./img/ui_customiser.png)

## Thanks
This was initially a Fork of https://github.com/wuyue92tree/django-adminlte-ui that we refactored so much we thought it
deserved its own package, big thanks to @wuyue92tree for all of his initial hard work, we are still patching into that
project were possible, but this project is taking a slightly different direction.

- Based on AdminLTE 3: https://adminlte.io/
- Using Bootstrap 4: https://getbootstrap.com/
- Using Font Awesome 5: https://fontawesome.com/
