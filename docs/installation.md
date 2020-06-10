# Installation & Setup

## General use

Install the latest [pypi](https://pypi.org/project/django-jazzmin/) release with `pip install -U django-jazzmin`

Add `jazzmin` to your `INSTALLED_APPS` before `django.contrib.admin`, and voila!

```python
INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    [...]
]
```

See [configuration](./configuration.md) for customisation of the theme

## For development

    git clone git@github.com:farridav/django-jazzmin.git
    python3 -m venv .venv
    . .venv/bin/activate
    pip install -r dev-requirements.txt

See [development](./development.md) for notes on development
