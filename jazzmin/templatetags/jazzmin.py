import copy
import itertools
import logging
import urllib.parse

from django.contrib.admin.views.main import PAGE_VAR
from django.contrib.auth import get_user_model
from django.template import Library
from django.template.loader import get_template
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .. import version
from ..settings import get_settings
from ..utils import order_with_respect_to, get_filter_id, get_custom_url, get_admin_url, get_model_permissions

User = get_user_model()
register = Library()
logger = logging.getLogger(__name__)
OPTIONS = get_settings()


@register.simple_tag(takes_context=True)
def get_side_menu(context):
    """
    Get the list of apps and models to render out in the side menu and on the dashboard page
    """
    user = context.get('user')
    if not user:
        return []

    model_permissions = get_model_permissions(user)

    menu = []
    available_apps = copy.deepcopy(context.get('available_apps', []))
    for app in available_apps:
        app_label = app['app_label'].lower()
        if app_label in OPTIONS['hide_apps']:
            continue

        allowed_models = []
        for model in app.get('models', []):
            model_str = '{app_label}.{model}'.format(app_label=app_label, model=model["object_name"]).lower()
            if model_str not in model_permissions:
                continue
            if model_str in OPTIONS.get('hide_models', []):
                continue

            model['icon'] = OPTIONS.get('icons', {}).get(model_str)
            allowed_models.append(model)

        for custom_link in OPTIONS.get('custom_links', {}).get(app_label, []):

            perm_matches = []
            for perm in custom_link.get('permissions', []):
                perm_matches.append(user.has_perm(perm))

            if not all(perm_matches):
                continue

            allowed_models.append({
                'custom': True,
                'name': custom_link.get('name'),
                'admin_url': get_custom_url(custom_link.get('url')),
                'icon': custom_link.get('icon'),
            })

        if len(allowed_models):
            app['models'] = allowed_models
            menu.append(app)

    if OPTIONS.get('order_with_respect_to'):
        menu = order_with_respect_to(menu, OPTIONS['order_with_respect_to'])

    return menu


@register.simple_tag
def get_top_menu(user):
    if not user:
        return []

    model_permissions = get_model_permissions(user)

    menu = []
    for item in get_settings().get('topmenu_links', []):

        perm_matches = []
        for perm in item.get('permissions', []):
            perm_matches.append(user.has_perm(perm))

        if not all(perm_matches):
            continue

        if item.get('model') and item.get('model').lower() not in model_permissions:
            continue

        if item.get('app'):
            item['app_children'] = list(filter(lambda x: x['model'] in model_permissions, item['app_children']))
            if len(item['app_children']) == 0:
                continue

        menu.append(item)

    return menu


@register.simple_tag
def get_jazzmin_settings():
    """
    Return Jazzmin settings
    """
    return OPTIONS


@register.simple_tag
def get_jazzmin_version():
    """
    Get the version for this package
    """
    return version


@register.simple_tag
def get_user_avatar(user):
    """
    For the given user, try to get the avatar image
    """
    no_avatar = static("adminlte/img/user2-160x160.jpg")

    if not OPTIONS.get('user_avatar'):
        return no_avatar

    avatar_field = getattr(user, OPTIONS['user_avatar'], None)
    if avatar_field:
        return avatar_field.url

    return no_avatar


@register.simple_tag
def jazzmin_paginator_number(cl, i):
    """
    Generate an individual page index link in a paginated list.
    """
    if i == '.':
        return format_html(
            '<li class="page-item">'
            '<a class="page-link" href="javascript:void(0);" data-dt-idx="3" tabindex="0">… </a>'
            '</li>'
        )

    elif i == cl.page_num:
        return format_html(("""
            <li class="page-item active">
            <a class="page-link" href="javascript:void(0);" data-dt-idx="3" tabindex="0">{num}
            </a>
            </li>
        """.format(num=i + 1)))

    else:
        query_string = cl.get_query_string({PAGE_VAR: i})
        end = mark_safe('end' if i == cl.paginator.num_pages - 1 else '')
        return format_html(("""
            <li class="page-item">
            <a href="{query_string}" class="page-link {end}" data-dt-idx="3" tabindex="0">{num}</a>
            </li>
        """).format(num=i + 1, query_string=query_string, end=end))


@register.simple_tag
def admin_extra_filters(cl):
    """
    Return the dict of used filters which is not included in list_filters form
    """
    used_parameters = list(itertools.chain(*(s.used_parameters.keys() for s in cl.filter_specs)))
    return dict((k, v) for k, v in cl.params.items() if k not in used_parameters)


@register.simple_tag
def jazzmin_list_filter(cl, spec):
    tpl = get_template(spec.template)
    choices = list(spec.choices(cl))
    field_key = get_filter_id(spec)
    matched_key = field_key
    for choice in choices:
        query_string = choice['query_string'][1:]
        query_parts = urllib.parse.parse_qs(query_string)

        value = ''
        matches = {}
        for key in query_parts.keys():
            if key == field_key:
                value = query_parts[key][0]
                matched_key = key
            elif key.startswith(field_key + '__') or '__' + field_key + '__' in key:
                value = query_parts[key][0]
                matched_key = key

            if value:
                matches[matched_key] = value

        # Iterate matches, use first as actual values, additional for hidden
        i = 0
        for key, value in matches.items():
            if i == 0:
                choice['name'] = key
                choice['value'] = value
            i += 1

    return tpl.render({'field_name': field_key, 'title': spec.title, 'choices': choices, 'spec': spec, })


@register.filter
def jazzy_admin_url(value):
    """
    Get the admin url for a given object
    """
    return get_admin_url(value)


@register.filter
def debug(value):
    """
    Add in a breakpoint here and use filter in templates for debugging ;)
    """
    return type(value)


@register.simple_tag
def sidebar_status(request):
    """
    Check if our sidebar is open or closed
    """
    if request.COOKIES.get('jazzy_menu', '') == 'closed':
        return 'sidebar-collapse'
    return ''


@register.filter
def can_view_self(perms):
    view_perm = '{}.view_{}'.format(User._meta.app_label, User._meta.model_name)
    change_perm = '{}.change_{}'.format(User._meta.app_label, User._meta.model_name)

    return perms[User._meta.app_label][view_perm] or perms[User._meta.app_label][change_perm]


@register.simple_tag
def header_class(header, forloop):
    classes = []
    sorted, asc, desc = header.get('sorted'), header.get('ascending'), header.get('descending')

    if forloop['counter0'] == 0:
        classes.append("djn-checkbox-select-all")

    if not header['sortable']:
        return ' '.join(classes)

    if sorted and asc:
        classes.append("sorting_asc")
    elif sorted and desc:
        classes.append("sorting_desc")
    else:
        classes.append("sorting")

    return ' '.join(classes)
