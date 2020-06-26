from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

__all__ = ["JazzminConfig"]


class JazzminConfig(AppConfig):
    name = "jazzmin"
    label = "jazzmin"
    verbose_name = _("Jazzmin")
