# Jazzmin

Welcome to Jazzmin, intended as a drop-in app to jazz up your django admin site, with plenty of things you can easily
customise, including a built-in UI customizer

## Features

- Drop-in admin skin, all configuration optional
- Select2 drop-downs
- Bootstrap 4 & AdminLTE UI components
- Search bar for any given model admin
- Modal windows instead of popups
- Customisable side menu
- Customisable top menu
- Customisable user menu
- Responsive
- Customisable UI (via Live UI changes, or custom CSS/JS)
- Based on the latest [adminlte](https://adminlte.io/) + [bootstrap](https://getbootstrap.com/)

## Demo

You can view the demo app by cloning the repository, and running the following commands:

```bash
    poetry install
 ./tests/test_app/manage.py migrate
 ./tests/test_app/manage.py reset
 ./tests/test_app/manage.py runserver_plus
```

## Screenshots

### Dashboard

[![dashboard](./img/dashboard.png)](./img/dashboard.png)

### List view

[![table list](./img/list_view.png)](./img/list_view.png)

### Detail view

[![form page](./img/detail_view.png)](./img/detail_view.png)

### History page

[![history page](./img/history_page.png)](./img/history_page.png)

### Modal windows

[![Modal windows](./img/related_modal_bootstrap.png)](./img/related_modal_bootstrap.png)

### Login view

[![login](./img/login.png)](./img/login.png)

### UI Customiser

[![UI Customiser](./img/ui_customiser.png)](./img/ui_customiser.png)

### Mobile layout

[![Mobile layout](./img/dashboard_mobile.png)](./img/dashboard_mobile.png)

### Tablet layout

[![Table Layout](./img/dashboard_tablet.png)](./img/dashboard_tablet.png)

### Admin docs (if installed)

[![Admin docs](./img/admin_docs.png)](./img/admin_docs.png)

## Thanks

This was initially a Fork of <https://github.com/wuyue92tree/django-adminlte-ui> that we refactored so much we thought it
deserved its own package, big thanks to @wuyue92tree for all of his initial hard work, we are still patching into that
project were possible, but this project is taking a slightly different direction.

- Based on AdminLTE 3: <https://adminlte.io/>
- Using Bootstrap 4: <https://getbootstrap.com/>
- Using Font Awesome 5: <https://fontawesome.com/>
