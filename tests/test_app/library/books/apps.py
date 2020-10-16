from django.apps import AppConfig
from django.conf import settings


class BooksConfig(AppConfig):
    name = "{}library.books".format(settings.PREFIX)
