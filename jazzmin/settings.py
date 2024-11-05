import logging
from typing import Any, Union

from django.conf import settings

from .types import JazzminSettings, UITweaks

logger = logging.getLogger(__name__)


def get_settings() -> JazzminSettings:
    jazzmin_settings: Union[JazzminSettings, dict[str, Any], None] = getattr(settings, "JAZZMIN_SETTINGS")
    if isinstance(jazzmin_settings, dict):
        jazzmin_settings = JazzminSettings(**jazzmin_settings)
    elif not jazzmin_settings:
        jazzmin_settings = JazzminSettings()

    return jazzmin_settings


def get_ui_tweaks() -> UITweaks:
    tweaks: Union[UITweaks, dict[str, Any], None] = getattr(settings, "JAZZMIN_UI_TWEAKS")
    if isinstance(tweaks, dict):
        tweaks = UITweaks(**tweaks)
    elif not tweaks:
        tweaks = UITweaks()

    return tweaks
