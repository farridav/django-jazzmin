import copy

from django import template
from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.urls import reverse

from .. import version

User = get_user_model()
register = template.Library()


def get_admin_url(model):
    """
    Return the admin URL for the given <app>.<model>
    """
    app_label, model_name = model.split('.')
    return reverse("admin:%s_%s_changelist" % (app_label, model_name))


DEFAULT_SETTINGS = {
    'demo': True,
    'search_form': True,
    'skin': 'blue',
    'site_title': AdminSite.site_title,
    'site_header': AdminSite.site_header,
    'site_logo': 'admin/dist/img/default-log.svg',
    'welcome_sign': 'Welcome',
    'copyright': 'Acme Ltd',
    'navigation_expanded': True,
    'search_model': 'auth.user',

    # To implement
    'hide_apps': ['auth', 'main'],
    'hide_models': ['auth.user', 'auth.groups'],
    'icons': {
        'auth': 'fa-people',
        'auth.user': 'fa-user',
    }
}


@register.simple_tag
def get_adminlte_settings():
    adminlte_settings = copy.deepcopy(DEFAULT_SETTINGS)
    user_settings = getattr(settings, 'ADMINLTE_SETTINGS')
    adminlte_settings.update(user_settings)

    if adminlte_settings['search_model']:
        adminlte_settings['search_model'] = get_admin_url(adminlte_settings['search_model'])

    return adminlte_settings


@register.simple_tag
def get_adminlte_version():
    return version
