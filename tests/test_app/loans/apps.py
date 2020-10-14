from django.apps import AppConfig
from django.conf import settings


class LoansConfig(AppConfig):
    name = f"{settings.PREFIX}loans"
