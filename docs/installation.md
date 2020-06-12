# Installation

Install the latest [pypi](https://pypi.org/project/django-jazzmin/) release with `pip install -U django-jazzmin`

Add `jazzmin` to your `INSTALLED_APPS` before `django.contrib.admin`, and Voila!

```python
INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    [...]
]
```

See [configuration](./configuration.md) for optional customisation of the theme

See [development](./development.md) for notes on setting up for development
