import logging

import django
from django import template

from .adminlte_options import get_adminlte_settings
from ..compat import get_available_apps

logger = logging.getLogger(__name__)

register = template.Library()
if django.VERSION < (1, 9):
    simple_tag = register.assignment_tag
else:
    simple_tag = register.simple_tag


@simple_tag(takes_context=True)
def get_menu(context, request, position='left'):
    """
    TODO:
        make top menu work nicely
        check user permissions here
    """
    options = get_adminlte_settings()

    # TODO: remove this and fix the shit top menu
    if position != 'left':
        return []

    available_apps = get_available_apps(request, context)

    for app in available_apps:
        for model in app.get('models', []):
            model['icon'] = options.get('icons', {}).get(app['app_label'], {}).get(model['name'].lower())

    return available_apps
