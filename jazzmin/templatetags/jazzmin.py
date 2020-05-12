import itertools
import logging
import urllib.parse

import django
from django.contrib.admin.views.main import PAGE_VAR
from django.contrib.auth import get_user_model
from django.template import Library
from django.template.loader import get_template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .. import version
from ..compat import get_available_apps
from ..settings import get_settings
from ..utils import order_with_respect_to, get_filter_id

User = get_user_model()
register = Library()
logger = logging.getLogger(__name__)
OPTIONS = get_settings()

if django.VERSION < (1, 9):
    simple_tag = register.assignment_tag
else:
    simple_tag = register.simple_tag


@simple_tag(takes_context=True)
def get_menu(context, request):
    permissions = set()
    for permission in request.user.get_all_permissions():
        app_label, model = permission.split('.')
        model = model.split('_')[1]
        permissions.add(f'{app_label}.{model}')

    available_apps = []
    all_apps = get_available_apps(request, context)

    for app in all_apps:
        app_label = app['app_label'].lower()
        if app_label in OPTIONS['hide_apps']:
            continue

        allowed_models = []
        for model in app.get('models', []):
            model_str = f'{app_label}.{model["object_name"]}'.lower()
            if model_str not in permissions:
                continue
            if model_str in OPTIONS.get('hide_models', []):
                continue

            model['icon'] = OPTIONS.get('icons', {}).get(model_str)
            allowed_models.append(model)

        for custom_link in OPTIONS.get('custom_links', {}).get(app_label, []):

            for perm in custom_link.get('permissions', []):
                if not request.user.has_perm(perm):
                    continue

            allowed_models.append({
                'name': custom_link.get('name'),
                'admin_url': custom_link.get('url'),
                'icon': custom_link.get('icon'),
            })

        if len(allowed_models):
            app['models'] = allowed_models
            available_apps.append(app)

    if OPTIONS.get('order_with_respect_to'):
        available_apps = order_with_respect_to(available_apps, OPTIONS['order_with_respect_to'])

    return available_apps


@register.simple_tag
def get_jazzmin_settings():
    return OPTIONS


@register.simple_tag
def get_jazzmin_version():
    return version


@register.simple_tag
def get_user_avatar(user):
    no_avatar = '<i class="jazzmin-avatar fa fa-user fa-inverse"></i>'

    if not OPTIONS.get('user_avatar'):
        return format_html(no_avatar)

    avatar_field = getattr(user, OPTIONS['user_avatar'], None)
    if avatar_field:
        return f'<img src="{avatar_field.url}" class="img-circle" alt="User Image">'

    return format_html(no_avatar)


@register.simple_tag
def jazzmin_paginator_number(cl, i):
    """
    Generate an individual page index link in a paginated list.
    """
    if i == '.':
        return format_html(
            '<li class="paginate_button">'
            '<a href="javascript:void(0);" aria-controls="example2" data-dt-idx="3" tabindex="0">… </a>'
            '</li>'
        )

    elif i == cl.page_num:
        return format_html(
            '<li class="paginate_button active">'
            f'<a href="javascript:void(0);" aria-controls="example2" data-dt-idx="3" tabindex="0">{i + 1}</a>'
            '</li>'
        )

    else:
        query_string = cl.get_query_string({PAGE_VAR: i})
        classes = mark_safe(' class="end"' if i == cl.paginator.num_pages - 1 else '')
        return format_html(
            '<li class="paginate_button">'
            f'<a href="{query_string}" {classes} aria-controls="example2" data-dt-idx="3" tabindex="0">{i + 1}</a>'
            '</li>'
        )


@register.simple_tag
def admin_extra_filters(cl):
    """
    Return the dict of used filters which is not included in list_filters form
    """
    used_parameters = list(itertools.chain(*(s.used_parameters.keys() for s in cl.filter_specs)))
    return dict((k, v) for k, v in cl.params.items() if k not in used_parameters)


@register.simple_tag
def jazzmin_admin_list_filter(cl, spec):
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
