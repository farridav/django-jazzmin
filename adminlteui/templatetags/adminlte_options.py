from django import template
from django.conf import settings

from .. import version
from ..models import Options

register = template.Library()


@register.simple_tag
def get_adminlte_option(option_name, request=None):
    config = Options.objects.filter(valid=True, option_name=option_name).first()
    ret = {}

    if config:
        ret = {
            config.option_name: config.option_value,
        }
        if config.option_name in ('site_logo',):
            ret[config.option_name] = f'{settings.MEDIA_URL}{ret[config.option_name]}'

    return ret


@register.simple_tag
def get_adminlte_settings():
    # repo_link = f'https://github.com/wuyue92tree/django-adminlte-ui/tree/{version}'

    return getattr(settings, 'ADMINLTE_SETTINGS', {
        'demo': True,
        'search_form': True,
        'skin': 'blue',

        # f'copyright': '<a href="{repo_link}">django-adminlte-ui {version}</a>',
        # 'navigation_expanded': True,
        #
        # # if you are use custom menu, which will not effective below!
        # 'show_apps': ['django_admin_settings', 'auth', 'main'],

        'main_navigation_app': 'django_admin_settings',
        'icons': {
            'myapp': {
                'shops': 'fa-shopping-cart',
                'products': 'fa-dollar',
            }
        }
    })


@register.simple_tag
def get_adminlte_version():
    return version
