from django.apps import AppConfig


class BooksConfig(AppConfig):
    name = "tests.test_app.library.books"

    def ready(self) -> None:
        from . import receivers  # NOQA
