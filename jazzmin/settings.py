import copy
import logging
from typing import Any, Dict

from django.conf import settings
from django.templatetags.static import static

from .utils import get_admin_url, get_model_meta

logger = logging.getLogger(__name__)

DEFAULT_SETTINGS: Dict[str, Any] = {
    # title of the window (Will default to current_admin_site.site_title)
    "site_title": None,
    # Title on the login screen (19 chars max) (will default to current_admin_site.site_header)
    "site_header": None,
    # Title on the brand (19 chars max) (will default to current_admin_site.site_header)
    "site_brand": None,
    # Relative path to logo for your site, used for brand on top left (must be present in static files)
    "site_logo": "vendor/adminlte/img/AdminLTELogo.png",
    # Relative path to logo for your site, used for login logo (must be present in static files. Defaults to site_logo)
    "login_logo": None,
    # Logo to use for login form in dark themes (must be present in static files. Defaults to login_logo)
    "login_logo_dark": None,
    # CSS classes that are applied to the logo
    "site_logo_classes": "img-circle",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,
    # Welcome text on the login screen
    "welcome_sign": "Welcome",
    # Copyright on the footer
    "copyright": "",
    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": None,
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,
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
    # Custom icons for side menu apps/models See the link below
    # https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,
    # 5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,
    # 5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {"auth": "fas fa-users-cog", "auth.user": "fas fa-user", "auth.Group": "fas fa-users"},
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
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
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

DEFAULT_UI_TWEAKS: Dict[str, Any] = {
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
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
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


def get_search_model_string(search_model: str) -> str:
    """
    Get a search model string for reversing an admin url.

    Ensure the model name is lower cased but remain the app name untouched.
    """

    app, model_name = search_model.split(".")
    return "{app}.{model_name}".format(app=app, model_name=model_name.lower())


def get_settings() -> Dict:
    jazzmin_settings = copy.deepcopy(DEFAULT_SETTINGS)
    user_settings = {x: y for x, y in getattr(settings, "JAZZMIN_SETTINGS", {}).items() if y is not None}
    jazzmin_settings.update(user_settings)

    # Extract search model configuration from search_model setting
    if jazzmin_settings["search_model"]:
        if not isinstance(jazzmin_settings["search_model"], list):
            jazzmin_settings["search_model"] = [jazzmin_settings["search_model"]]

        jazzmin_settings["search_models_parsed"] = []
        for search_model in jazzmin_settings["search_model"]:
            jazzmin_search_model = {}
            jazzmin_search_model["search_url"] = get_admin_url(get_search_model_string(search_model))

            model_meta = get_model_meta(search_model)
            if model_meta:
                jazzmin_search_model["search_name"] = model_meta.verbose_name_plural.title()
            else:
                jazzmin_search_model["search_name"] = search_model.split(".")[-1] + "s"
            jazzmin_settings["search_models_parsed"].append(jazzmin_search_model)

    # Deal with single strings in hide_apps/hide_models and make sure we lower case 'em
    if isinstance(jazzmin_settings["hide_apps"], str):
        jazzmin_settings["hide_apps"] = [jazzmin_settings["hide_apps"]]
    jazzmin_settings["hide_apps"] = [x.lower() for x in jazzmin_settings["hide_apps"]]

    if isinstance(jazzmin_settings["hide_models"], str):
        jazzmin_settings["hide_models"] = [jazzmin_settings["hide_models"]]
    jazzmin_settings["hide_models"] = [x.lower() for x in jazzmin_settings["hide_models"]]

    # Ensure icon model names and classes are lower case
    jazzmin_settings["icons"] = {x.lower(): y.lower() for x, y in jazzmin_settings.get("icons", {}).items()}

    # Default the site icon using the site logo
    jazzmin_settings["site_icon"] = jazzmin_settings["site_icon"] or jazzmin_settings["site_logo"]

    # Default the login logo using the site logo
    jazzmin_settings["login_logo"] = jazzmin_settings["login_logo"] or jazzmin_settings["site_logo"]

    # Default the login logo dark using the login logo
    jazzmin_settings["login_logo_dark"] = jazzmin_settings["login_logo_dark"] or jazzmin_settings["login_logo"]

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

    ret = {
        "raw": raw_tweaks,
        "theme": {"name": theme, "src": static(THEMES[theme])},
        "sidebar_classes": classes("sidebar", "sidebar_disable_expand"),
        "navbar_classes": classes("navbar", "no_navbar_border", "navbar_small_text"),
        "body_classes": classes(
            "accent", "body_small_text", "navbar_fixed", "footer_fixed", "sidebar_fixed", "layout_boxed"
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

    if dark_mode_theme:
        ret["dark_mode_theme"] = {"name": dark_mode_theme, "src": static(THEMES[dark_mode_theme])}

    return ret
