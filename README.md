# Django jazzmin (Jazzy Admin)
Drop-in theme for django admin, that utilises AdminLTE 3 & Bootstrap 4 to make yo' admin looky jazzy

Support for custom or generated menus on the left or the top.

## Features
- drop-in, configure only if you want to
- Customisable side menu
- Customisable top menu
- Customisable UI (via Live UI changes, or custom CSS/JS)
- Based on the latest [adminlte](https://adminlte.io/) + [bootstrap](https://getbootstrap.com/)

## Screenshots

## Dashboard
![dashboard](docs/img/dashboard.png)

## List view
![table list](docs/img/list_view.png)

## Detail view
![form page](docs/img/detail_view.png)

## Login view
![login](docs/img/login.png)

## Installation
```
pip install django-jazzmin
```

## Setup & configuration
See [test_app](./tests/test_app/settings.py) or [docs](https://django-jazzmin.readthedocs.io/)

# Thanks
This was initially a Fork of https://github.com/wuyue92tree/django-adminlte-ui that we refactored so much we thought it
deserved its own package, big thanks to @wuyue92tree for all of his initial hard work, we are still patching into that
project were possible, but this project is taking a slightly different direction.

- Based on AdminLTE 3: https://adminlte.io/
- Using Bootstrap 4: https://getbootstrap.com/
- Using Font Awesome 5: https://fontawesome.com/
