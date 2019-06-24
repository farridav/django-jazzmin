from django.template import Library
from django.template.loader import get_template
import urllib.parse

register = Library()


@register.simple_tag
def adminlte_admin_list_filter(cl, spec):
    tpl = get_template(spec.template)
    new_choice = []

    print(spec.lookup_kwarg)
    print(list(spec.choices(cl)))

    for choice in list(spec.choices(cl)):
        qs = (urllib.parse.parse_qs(choice.get('query_string')))
        # print(qs)
        for k, v in qs.items():
            if k.strip('?') in cl.params.keys() and k.strip(
                    '?') != spec.lookup_kwarg:
                continue
            new_choice.append({'name': k.strip('?'), 'value': v[0],
                               'display': choice.get('display'),
                               'selected': choice.get('selected')})

    print(new_choice)

    return tpl.render({
        'title': spec.title,
        'choices': list(spec.choices(cl)),
        'new_choices': new_choice,
        'spec': spec,
    })

# def adminlte_search_form(cl):
#     """
#     Display a search form for searching the list.
#     """
#     print(cl)
#     return {
#         'cl': cl,
#         'show_result_count': cl.result_count != cl.full_result_count,
#         'search_var': SEARCH_VAR
#     }
#
#
# @register.tag(name='adminlte_search_form')
# def adminlte_search_form_tag(parser, token):
#     return InclusionAdminNode(parser, token, func=adminlte_search_form,
#                               template_name='search_form.html',
#                               takes_context=False)
