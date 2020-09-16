from django.apps import AppConfig
from django.conf import settings


class UtilsConfig(AppConfig):
    name = f"{settings.PREFIX}utils"
