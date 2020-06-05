import copy

from django.conf import settings
from django.contrib.admin import AdminSite

from .utils import get_admin_url, get_custom_url, get_model_meta, get_app_admin_urls

DEFAULT_SETTINGS = {
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

    # The model admin to search from the search bar, search bar omitted if excluded
    'search_model': None,

    # Field name on user model that contains avatar image
    'user_avatar': 'avatar',

    # Links to put along the top menu
    'topmenu_links': [],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    'show_sidebar': True,

    # Whether to aut expand the menu
    'navigation_expanded': True,

    # Hide these apps when generating side menu
    'hide_apps': [],

    # Hide these models when generating side menu
    'hide_models': [],

    # List of apps to base side menu ordering off of
    'order_with_respect_to': [],

    # Custom links to append to app groups, keyed on app name
    'custom_links': {},

    # Custom icons per model in the side menu See https://www.fontawesomecheatsheet.com/font-awesome-cheatsheet-5x/
    # for a list of icon classes
    'icons': {
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

    for link in jazzmin_settings.get('topmenu_links', []):
        if 'url' in link:
            link['url'] = get_custom_url(link['url'])
        elif 'model' in link:
            link['name'] = get_model_meta(link['model']).verbose_name_plural.title()
            link['url'] = get_admin_url(link['model'])
        elif 'app' in link:
            link['name'] = link['app'].title()
            link['app_children'] = get_app_admin_urls(link['app'])

    jazzmin_settings['hide_apps'] = [x.lower() for x in jazzmin_settings['hide_apps']]
    jazzmin_settings['hide_models'] = [x.lower() for x in jazzmin_settings['hide_models']]

    return jazzmin_settings
