import itertools
from django.contrib.admin.views.main import (
    ALL_VAR, ORDER_VAR, PAGE_VAR, SEARCH_VAR,
)
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.template import Library
from django.template.loader import get_template
import urllib.parse

register = Library()

DOT = '.'


@register.simple_tag
def adminlte_paginator_number(cl, i):
    """
    Generate an individual page index link in a paginated list.
    """
    if i == DOT:
        # <li class="paginate_button active"><a href="#" aria-controls="example2" data-dt-idx="3" tabindex="0">{}</a></li>'
        return format_html(
            '<li class="paginate_button"><a href="javascript:void(0);" aria-controls="example2" data-dt-idx="3" tabindex="0">… </a></li>')
    elif i == cl.page_num:
        return format_html(
            '<li class="paginate_button active"><a href="javascript:void(0);" aria-controls="example2" data-dt-idx="3" tabindex="0">{}</a></li>',
            i + 1)
    else:
        return format_html(
            '<li class="paginate_button "><a href="{}" {} aria-controls="example2" data-dt-idx="3" tabindex="0">{}</a></li>',
            cl.get_query_string({PAGE_VAR: i}),
            mark_safe(
                ' class="end"' if i == cl.paginator.num_pages - 1 else ''),
            i + 1,
        )


def get_filter_id(spec):
    try:
        return getattr(spec, 'field_path')
    except AttributeError:
        try:
            return getattr(spec, 'parameter_name')
        except AttributeError:
            pass
    return spec.title


@register.simple_tag
def admin_extra_filters(cl):
    """ Return the dict of used filters which is not included
    in list_filters form """
    used_parameters = list(itertools.chain(*(s.used_parameters.keys()
                                             for s in cl.filter_specs)))
    return dict(
        (k, v) for k, v in cl.params.items() if k not in used_parameters)


@register.simple_tag
def adminlte_admin_list_filter(cl, spec):
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
            elif key.startswith(
                    field_key + '__') or '__' + field_key + '__' in key:
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
            # else:
            #     choice['additional'] = '%s=%s' % (key, value)
            i += 1

    return tpl.render({
        'field_name': field_key,
        'title': spec.title,
        'choices': choices,
        'spec': spec,
    })
