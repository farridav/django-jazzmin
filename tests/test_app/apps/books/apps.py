from django.apps import AppConfig
from django.conf import settings


class BooksConfig(AppConfig):
    name = f"{settings.PREFIX}books"
