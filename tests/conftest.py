import copy

import pytest
from django.urls import reverse
from .test_app.library.factories import BookFactory


@pytest.fixture
def change_form_context(admin_client):
    book = BookFactory()
    url = reverse("admin:books_book_change", args=(book.pk,))
    response = admin_client.get(url)
    yield response.context


@pytest.fixture(scope="function")
def custom_jazzmin_settings(settings):
    original_settings = copy.deepcopy(settings.JAZZMIN_SETTINGS)
    settings.JAZZMIN_SETTINGS = original_settings
    yield original_settings
