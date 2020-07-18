import copy

from django.conf import settings
from django.contrib.admin import AdminSite

from .utils import get_admin_url, get_model_meta

DEFAULT_SETTINGS = {
    # title of the window
    "site_title": AdminSite.site_title,
    # Title on the brand, and the login screen (19 chars max)
    "site_header": AdminSite.site_header,
    # Relative path to logo for your site, used for favicon and brand on top left (must be present in static files)
    "site_logo": "adminlte/img/AdminLTELogo.png",
    # Welcome text on the login screen
    "welcome_sign": "Welcome",
    # Copyright on the footer
    "copyright": "",
    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": None,
    # Field name on user model that contains avatar image
    "user_avatar": "avatar",
    ############
    # Top Menu #
    ############
    # Links to put along the nav bar
    "topmenu_links": [],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ('app' url type is not allowed)
    "usermenu_links": [],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps to base side menu ordering off of
    "order_with_respect_to": [],
    # Custom links to append to side menu app groups, keyed on app name
    "custom_links": {},
    # Custom icons for side menu apps/models See https://www.fontawesomecheatsheet.com/font-awesome-cheatsheet-5x/
    # for a list of icon classes
    "icons": {"auth": "fa-users-cog", "auth.user": "fa-user", "auth.Group": "fa-users",},
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fa-chevron-circle-right",
    "default_icon_children": "fa-circle",
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {},
}

#######################################
# Currently available UI tweaks       #
# Use the UI builder to generate this #
#######################################

DEFAULT_UI_TWEAKS = {
    # Small text on the top navbar
    "navbar_small_text": False,
    # Small text on the footer
    "footer_small_text": False,
    # Small text everywhere
    "body_small_text": False,
    # Small text on the brand/logo
    "brand_small_text": False,
    # brand/logo background colour
    "brand_colour": False,
    # Link colour
    "accent": "accent-primary",
    # topmenu colour
    "navbar": "navbar-white navbar-light",
    # topmenu border
    "no_navbar_border": False,
    # sidemenu colour
    "sidebar": "sidebar-dark-primary",
    # sidemenu small text
    "sidebar_nav_small_text": False,
    # Disable expanding on hover of collapsed sidebar
    "sidebar_disable_expand": False,
    # Indent child menu items on sidebar
    "sidebar_nav_child_indent": False,
    # Use a compact sidebar
    "sidebar_nav_compact_style": False,
    # Use the AdminLTE2 style sidebar
    "sidebar_nav_legacy_style": False,
    # Use a flat style sidebar
    "sidebar_nav_flat_style": False,
}

CHANGEFORM_TEMPLATES = {
    "single": "jazzmin/includes/single.html",
    "carousel": "jazzmin/includes/carousel.html",
    "collapsible": "jazzmin/includes/collapsible.html",
    "horizontal_tabs": "jazzmin/includes/horizontal_tabs.html",
    "vertical_tabs": "jazzmin/includes/vertical_tabs.html",
}


def get_settings():
    jazzmin_settings = copy.deepcopy(DEFAULT_SETTINGS)
    user_settings = {x: y for x, y in getattr(settings, "JAZZMIN_SETTINGS", {}).items() if y is not None}
    jazzmin_settings.update(user_settings)

    # Extract search url from search model
    if jazzmin_settings["search_model"]:
        jazzmin_settings["search_url"] = get_admin_url(jazzmin_settings["search_model"].lower())
        model_meta = get_model_meta(jazzmin_settings["search_model"])
        if model_meta:
            jazzmin_settings["search_name"] = model_meta.verbose_name_plural.title()
        else:
            jazzmin_settings["search_name"] = jazzmin_settings["search_model"].split(".")[-1] + "s"

    # Deal with single strings in hide_apps/hide_models and make sure we lower case 'em
    if type(jazzmin_settings["hide_apps"]) == str:
        jazzmin_settings["hide_apps"] = [jazzmin_settings["hide_apps"]]
    jazzmin_settings["hide_apps"] = [x.lower() for x in jazzmin_settings["hide_apps"]]

    if type(jazzmin_settings["hide_models"]) == str:
        jazzmin_settings["hide_models"] = [jazzmin_settings["hide_models"]]
    jazzmin_settings["hide_models"] = [x.lower() for x in jazzmin_settings["hide_models"]]

    # Ensure icon model names and classes are lower case
    jazzmin_settings["icons"] = {x.lower(): y.lower() for x, y in jazzmin_settings.get("icons", {}).items()}

    # ensure all model names are lower cased
    jazzmin_settings["changeform_format_overrides"] = {
        x.lower(): y.lower() for x, y in jazzmin_settings.get("changeform_format_overrides", {}).items()
    }

    return jazzmin_settings


def get_ui_tweaks():
    raw_tweaks = copy.deepcopy(DEFAULT_UI_TWEAKS)
    raw_tweaks.update(getattr(settings, "JAZZMIN_UI_TWEAKS", {}))
    tweaks = {x: y for x, y in raw_tweaks.items() if y not in (None, "", False)}

    bool_map = {
        "navbar_small_text": "text-sm",
        "footer_small_text": "text-sm",
        "body_small_text": "text-sm",
        "brand_small_text": "text-sm",
        "sidebar_nav_small_text": "text-sm",
        "no_navbar_border": "border-bottom-0",
        "sidebar_disable_expand": "sidebar-no-expand",
        "sidebar_nav_child_indent": "nav-child-indent",
        "sidebar_nav_compact_style": "nav-compact",
        "sidebar_nav_legacy_style": "nav-legacy",
        "sidebar_nav_flat_style": "nav-flat",
    }

    for key, value in bool_map.items():
        if key in tweaks:
            tweaks[key] = value

    def classes(*args):
        return " ".join([tweaks.get(arg, "") for arg in args if arg]).strip()

    return {
        "raw": raw_tweaks,
        "body_classes": classes("accent", "body_small_text"),
        "sidebar_classes": classes("sidebar", "sidebar_disable_expand"),
        "navbar_classes": classes("navbar", "no_nav_border", "navbar_small_text"),
        "sidebar_list_classes": classes(
            "sidebar_nav_small_text",
            "sidebar_nav_flat_style",
            "sidebar_nav_legacy_style",
            "sidebar_nav_child_indent",
            "sidebar_nav_compact_style",
        ),
        "brand_classes": classes("brand_small_text", "brand_colour"),
        "footer_classes": classes("footer_small_text"),
    }
