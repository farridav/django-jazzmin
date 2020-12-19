import copy
import logging
from typing import Dict

from django.conf import settings
from django.contrib.admin import AdminSite
from django.templatetags.static import static

from .utils import get_admin_url, get_model_meta

logger = logging.getLogger(__name__)

DEFAULT_SETTINGS = {
    # title of the window
    "site_title": AdminSite.site_title,
    # Title on the brand, and the login screen (19 chars max)
    "site_header": AdminSite.site_header,
    # Relative path to logo for your site, used for favicon and brand on top left (must be present in static files)
    "site_logo": "vendor/adminlte/img/AdminLTELogo.png",
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
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free
    # for a list of icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #################
    # Related Modal #
    #################
    # Activate Bootstrap modal
    "related_modal_active": False,
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
    # Add a language dropdown into the admin
    "language_chooser": False,
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
    # Make the top navbar sticky, keeping it in view as you scroll
    "navbar_fixed": False,
    # Whether to constrain the page to a box (leaving big margins at the side)
    "layout_boxed": False,
    # Make the footer sticky, keeping it in view all the time
    "footer_fixed": False,
    # Make the sidebar sticky, keeping it in view as you scroll
    "sidebar_fixed": False,
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
    # Bootstrap theme to use (default, or from bootswatch, see THEMES below)
    "theme": "default",
    # Theme to use instead if the user has opted for dark mode (e.g darkly/cyborg/slate/solar/superhero)
    "dark_mode_theme": None,
    # The classes/styles to use with buttons
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success",
    },
}

THEMES = {
    # light themes
    "default": "vendor/bootswatch/default/bootstrap.min.css",
    "cerulean": "vendor/bootswatch/cerulean/bootstrap.min.css",
    "cosmo": "vendor/bootswatch/cosmo/bootstrap.min.css",
    "flatly": "vendor/bootswatch/flatly/bootstrap.min.css",
    "journal": "vendor/bootswatch/journal/bootstrap.min.css",
    "litera": "vendor/bootswatch/litera/bootstrap.min.css",
    "lumen": "vendor/bootswatch/lumen/bootstrap.min.css",
    "lux": "vendor/bootswatch/lux/bootstrap.min.css",
    "materia": "vendor/bootswatch/materia/bootstrap.min.css",
    "minty": "vendor/bootswatch/minty/bootstrap.min.css",
    "pulse": "vendor/bootswatch/pulse/bootstrap.min.css",
    "sandstone": "vendor/bootswatch/sandstone/bootstrap.min.css",
    "simplex": "vendor/bootswatch/simplex/bootstrap.min.css",
    "sketchy": "vendor/bootswatch/sketchy/bootstrap.min.css",
    "spacelab": "vendor/bootswatch/spacelab/bootstrap.min.css",
    "united": "vendor/bootswatch/united/bootstrap.min.css",
    "yeti": "vendor/bootswatch/yeti/bootstrap.min.css",
    # dark themes
    "darkly": "vendor/bootswatch/darkly/bootstrap.min.css",
    "cyborg": "vendor/bootswatch/cyborg/bootstrap.min.css",
    "slate": "vendor/bootswatch/slate/bootstrap.min.css",
    "solar": "vendor/bootswatch/solar/bootstrap.min.css",
    "superhero": "vendor/bootswatch/superhero/bootstrap.min.css",
}

DARK_THEMES = ("darkly", "cyborg", "slate", "solar", "superhero")

CHANGEFORM_TEMPLATES = {
    "single": "jazzmin/includes/single.html",
    "carousel": "jazzmin/includes/carousel.html",
    "collapsible": "jazzmin/includes/collapsible.html",
    "horizontal_tabs": "jazzmin/includes/horizontal_tabs.html",
    "vertical_tabs": "jazzmin/includes/vertical_tabs.html",
}


def get_search_model_string(jazzmin_settings: Dict) -> str:
    """
    Get a search model string for reversing an admin url.

    Ensure the model name is lower cased but remain the app name untouched.
    """

    app, model_name = jazzmin_settings["search_model"].split(".")
    return "{app}.{model_name}".format(app=app, model_name=model_name.lower())


def get_settings() -> Dict:
    jazzmin_settings = copy.deepcopy(DEFAULT_SETTINGS)
    user_settings = {x: y for x, y in getattr(settings, "JAZZMIN_SETTINGS", {}).items() if y is not None}
    jazzmin_settings.update(user_settings)

    # Extract search url from search model
    if jazzmin_settings["search_model"]:
        jazzmin_settings["search_url"] = get_admin_url(get_search_model_string(jazzmin_settings))
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


def get_ui_tweaks() -> Dict:
    raw_tweaks = copy.deepcopy(DEFAULT_UI_TWEAKS)
    raw_tweaks.update(getattr(settings, "JAZZMIN_UI_TWEAKS", {}))
    tweaks = {x: y for x, y in raw_tweaks.items() if y not in (None, "", False)}

    # These options dont work well together
    if tweaks.get("layout_boxed"):
        tweaks.pop("navbar_fixed", None)
        tweaks.pop("footer_fixed", None)

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
        "layout_boxed": "layout-boxed",
        "sidebar_fixed": "layout-fixed",
        "navbar_fixed": "layout-navbar-fixed",
        "footer_fixed": "layout-footer-fixed",
        "actions_sticky_top": "sticky-top",
    }

    for key, value in bool_map.items():
        if key in tweaks:
            tweaks[key] = value

    def classes(*args: str) -> str:
        return " ".join([tweaks.get(arg, "") for arg in args]).strip()

    theme = tweaks["theme"]
    if theme not in THEMES:
        logger.warning("{} not found in {}, using default".format(theme, THEMES.keys()))
        theme = "default"

    dark_mode_theme = tweaks.get("dark_mode_theme", None)
    if dark_mode_theme and dark_mode_theme not in DARK_THEMES:
        logger.warning("{} is not a dark theme, using darkly".format(dark_mode_theme))
        dark_mode_theme = "darkly"

    theme_body_classes = " theme-{}".format(theme)
    if theme in DARK_THEMES:
        theme_body_classes += " dark-mode"

    return {
        "raw": raw_tweaks,
        "theme": {"name": theme, "src": static(THEMES[theme])},
        "dark_mode_theme": {"name": dark_mode_theme, "src": static(THEMES[theme])},
        "sidebar_classes": classes("sidebar", "sidebar_disable_expand"),
        "navbar_classes": classes("navbar", "no_navbar_border", "navbar_small_text"),
        "body_classes": classes(
            "accent",
            "body_small_text",
            "navbar_fixed",
            "footer_fixed",
            "sidebar_fixed",
            "layout_boxed",
        )
        + theme_body_classes,
        "actions_classes": classes("actions_sticky_top"),
        "sidebar_list_classes": classes(
            "sidebar_nav_small_text",
            "sidebar_nav_flat_style",
            "sidebar_nav_legacy_style",
            "sidebar_nav_child_indent",
            "sidebar_nav_compact_style",
        ),
        "brand_classes": classes("brand_small_text", "brand_colour"),
        "footer_classes": classes("footer_small_text"),
        "button_classes": tweaks["button_classes"],
    }
