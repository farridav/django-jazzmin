import logging

import django
from django import template
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest
from django.urls import NoReverseMatch
from django.utils.translation import gettext_lazy as _

from .adminlte_options import get_adminlte_option, get_adminlte_settings
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

    return None


def get_custom_menu(user, position):
    """
    use content_type and user.permission control the menu

    `label:model`

    :param user:
    :return:
    """
    all_permissions = user.get_all_permissions()

    limit_for_internal_link = []
    for permission in all_permissions:
        app_label = permission.split('.')[0]
        model = permission.split('.')[1].split('_')[1]
        limit_for_internal_link.append(f'{app_label}:{model}')

    limit_for_internal_link = set(limit_for_internal_link)
    new_available_apps = []
    menu = Menu.get_tree().filter(depth=1).order_by('-priority_level')

    for menu_item in menu:
        if menu_item.position != position:
            continue

        new_available_apps_item = {}
        if menu_item.valid is False:
            continue

        new_available_apps_item['name'] = menu_item.name
        new_available_apps_item['icon'] = menu_item.icon

        children = menu_item.get_children().order_by('-priority_level')
        if not children:
            # skip menu_item that no children and link type is devide.
            if menu_item.link_type in (0, 1):
                new_available_apps_item['admin_url'] = get_reverse_link(menu_item.link)
                new_available_apps.append(new_available_apps_item)
            continue
        new_available_apps_item['models'] = []

        for children_item in children:
            if children_item.link_type == 0:
                # internal link should connect a content_type, otherwise it will be hide.
                if children_item.content_type:
                    obj = ContentType.objects.get(id=children_item.content_type.id)
                    # if user hasn't permission, the model will be skip.
                    if obj.app_label + ':' + obj.model not in limit_for_internal_link:
                        continue
                else:
                    continue

            if children_item.valid is False:
                continue
            new_children_item = dict()
            new_children_item['name'] = children_item.name
            new_children_item['admin_url'] = get_reverse_link(children_item.link)
            if not new_children_item['admin_url']:
                continue
            new_children_item['icon'] = children_item.icon
            new_available_apps_item['models'].append(new_children_item)
        if new_available_apps_item['models']:
            new_available_apps.append(new_available_apps_item)

    return new_available_apps


@simple_tag(takes_context=True)
def get_menu(context, request, position='left'):
    """
    :type request: WSGIRequest
    """
    if not isinstance(request, HttpRequest):
        return None

    user = getattr(request, 'user', None)

    use_custom_menu = get_adminlte_option('USE_CUSTOM_MENU')
    if use_custom_menu.get('USE_CUSTOM_MENU', '0') == '1':
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
