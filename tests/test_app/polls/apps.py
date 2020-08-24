from django.apps import AppConfig
from django.conf import settings


class PollsConfig(AppConfig):
    name = f"{settings.PREFIX}polls"
