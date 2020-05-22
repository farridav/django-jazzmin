import copy

from django.conf import settings
from django.contrib.admin import AdminSite

from .utils import get_admin_url

DEFAULT_SETTINGS = {
    # Choose from black, black-light, blue, blue-light, green, green-light, purple, purple-light
    # red, red-light, yellow, yellow-light
    'skin': 'blue',

    # title of the window
    'site_title': AdminSite.site_title,

    # Title on the login screen
    'site_header': AdminSite.site_header,

    # square logo to use for your site, must be present in static files, used for favicon and brand on top left
    'site_logo': 'adminlte/img/AdminLTELogo.png',

    # Welcome text on the login screen
    'welcome_sign': 'Welcome',

    # Copyright on the footer
    'copyright': '',

    # Whether to aut expand the menu
    'navigation_expanded': True,

    # The model admin to search from the search bar, search bar omitted if excluded
    'search_model': None,

    # Field name on user model that contains avatar image
    'user_avatar': 'avatar',

    # Hide these apps when generating menu
    'hide_apps': [],

    # Hide these models when generating menu
    'hide_models': [],

    # List of apps to base menu ordering off of
    'order_with_respect_to': [],

    # Custom links to append to app groups, keyed on app name
    'custom_links': {},

    # Custom icons per app or model
    'icons': {
        'auth': 'fa-people',
        'auth.user': 'fa-user',
    }
}


def get_settings():
    jazzmin_settings = copy.deepcopy(DEFAULT_SETTINGS)
    user_settings = {x: y for x, y in getattr(settings, 'JAZZMIN_SETTINGS', {}).items() if y is not None}
    jazzmin_settings.update(user_settings)

    if jazzmin_settings['search_model']:
        jazzmin_settings['search_url'] = get_admin_url(jazzmin_settings['search_model'].lower())
        jazzmin_settings['search_name'] = jazzmin_settings['search_model'].split('.')[-1] + 's'

    jazzmin_settings['hide_apps'] = [x.lower() for x in jazzmin_settings['hide_apps']]
    jazzmin_settings['hide_models'] = [x.lower() for x in jazzmin_settings['hide_models']]

    return jazzmin_settings
