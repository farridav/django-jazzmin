from django import template
from django.conf import settings

from .. import version
from ..models import Options

register = template.Library()

DEFAULT_SETTINGS = {
    'demo': True,
    'search_form': True,
    'skin': 'blue',

    # 'copyright': 'Acme Ltd',
    # 'navigation_expanded': True,

    # if you are use custom menu, this will be ignored!
    # 'show_apps': ['django_admin_settings', 'auth', 'main'],

    'main_navigation_app': 'django_admin_settings',
    'icons': {
        'myapp': {
            'shops': 'fa-shopping-cart',
            'products': 'fa-dollar',
        }
    }
}


@register.simple_tag
def get_adminlte_options():
    options = Options.as_dict()
    logo = options.get('site_logo')
    if logo:
        options['site_logo'] = f'{settings.MEDIA_URL}{logo}'

    return options


@register.simple_tag
def get_adminlte_settings():
    return getattr(settings, 'ADMINLTE_SETTINGS', DEFAULT_SETTINGS)


@register.simple_tag
def get_adminlte_version():
    return version
