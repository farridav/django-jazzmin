import logging

import django
from django import template
from django.http import HttpRequest
from django.urls import NoReverseMatch
from django.utils.translation import gettext_lazy as _

from .adminlte_options import get_adminlte_options, get_adminlte_settings
from ..compat import reverse, get_available_apps
from ..models import Menu

logger = logging.getLogger(__name__)

register = template.Library()
if django.VERSION < (1, 9):
    simple_tag = register.assignment_tag
else:
    simple_tag = register.simple_tag


def get_reverse_link(link):
    if not link or '/' in link:
        return link

    try:
        return reverse(link)
    except NoReverseMatch:
        pass

    return '#bad_link'


def get_custom_menu(user, position):
    permissions = set()
    for permission in user.get_all_permissions():
        app_label, model = permission.split('.')
        model = model.split('_')[1]
        permissions.add(f'{app_label}:{model}')

    menu = Menu.get_tree().filter(depth=1, position=position).order_by('-priority_level')

    menu_list = []
    for item in menu:
        menu_list_item = {
            'name': item.name,
            'icon': item.icon,
            'admin_url': get_reverse_link(item.link),
            'models': []
        }

        # Links with no children
        children = item.get_children().select_related('model').order_by('-priority_level')
        for child_item in children:

            # if user hasn't permission, skip the link
            if child_item.model and f'{child_item.model.app_label}:{child_item.model.model}' not in permissions:
                continue

            menu_list_item['models'].append({
                'name': child_item.name,
                'admin_url': get_reverse_link(child_item.link),
                'icon': child_item.icon
            })

        menu_list.append(menu_list_item)

    return menu_list


@simple_tag(takes_context=True)
def get_menu(context, request, position='left'):
    user = getattr(request, 'user', None)

    options = get_adminlte_options()
    if options.get('USE_CUSTOM_MENU', '0') == '1':
        return get_custom_menu(user, position)

    if position != 'left':
        return []

    available_apps = get_available_apps(request, context)

    for app in available_apps:
        if app.get('app_label') == 'django_admin_settings':
            permissions = ['django_admin_settings.add_options', 'django_admin_settings.change_options']

            if any(user.has_perm(perm) for perm in permissions):
                app.get('models').insert(0, {
                    'name': _('General Options'),
                    'object_name': 'Options',
                    'perms': {
                        'add': True,
                        'change': True,
                        'delete': True,
                        'view': True
                    },
                    'admin_url': reverse('admin:general_option'),
                    'view_only': False
                })
        else:
            for model in app.get('models', []):
                model['icon'] = get_adminlte_settings().get(
                    'icons', {}
                ).get(app['app_label'], {}).get(model['name'].lower())

    return available_apps
