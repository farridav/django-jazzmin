import logging
from typing import Any, Union

from django.conf import settings
from django.templatetags.static import static

from jazzmin.types import JazzminSettings

from .types import DarkThemes, UITweaks

logger = logging.getLogger(__name__)


def get_settings() -> JazzminSettings:
    jazzmin_settings: Union[JazzminSettings, dict[str, Any], None] = getattr(settings, "JAZZMIN_SETTINGS")
    if isinstance(jazzmin_settings, dict):
        jazzmin_settings = JazzminSettings(**jazzmin_settings)

    if not jazzmin_settings:
        jazzmin_settings = JazzminSettings()

    return jazzmin_settings


def get_ui_tweaks() -> UITweaks:
    tweaks: Union[UITweaks, dict[str, Any], None] = getattr(settings, "JAZZMIN_UI_TWEAKS")
    if isinstance(tweaks, dict):
        tweaks = UITweaks(**tweaks)
    elif not tweaks:
        tweaks = UITweaks()

    # These options dont work well together
    if tweaks.layout_boxed:
        tweaks.navbar_fixed = False
        tweaks.footer_fixed = False

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
    theme_body_classes = " theme-{}".format(theme)
    if theme in DarkThemes.__members__:
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
