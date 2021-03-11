from unittest import mock

import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from jazzmin.settings import CHANGEFORM_TEMPLATES

from .test_app.library.factories import BookFactory, UserFactory
from .test_app.library.books.admin import BookAdmin
from .utils import override_jazzmin_settings


@pytest.mark.django_db
def test_update_site_logo(admin_client, settings):
    """
    We can add a site logo, and it renders out
    """
    url = reverse("admin:index")

    settings.JAZZMIN_SETTINGS["site_logo"] = "books/img/logo.png"
    response = admin_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    assert soup.find("a", class_="brand-link").find("img")["src"] == "/static/books/img/logo.png"


@pytest.mark.django_db
@pytest.mark.parametrize("config_value,template", [(k, v) for k, v in CHANGEFORM_TEMPLATES.items()])
def test_changeform_templates(admin_client, settings, config_value, template):
    """
    All changeform config values use the correct templates
    """
    book = BookFactory()

    url = reverse("admin:books_book_change", args=(book.pk,))

    settings.JAZZMIN_SETTINGS = override_jazzmin_settings(changeform_format=config_value)

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]

    assert template in templates_used


@pytest.mark.django_db
def test_changeform_template_override(admin_client, settings):
    """
    We can set a global template, and override it per model
    """
    user = UserFactory()
    book = BookFactory()

    books_url = reverse("admin:books_book_change", args=(book.pk,))
    users_url = reverse("admin:auth_user_change", args=(user.pk,))

    settings.JAZZMIN_SETTINGS = override_jazzmin_settings(
        changeform_format="vertical_tabs",
        changeform_format_overrides={"books.book": "carousel"},
    )

    response = admin_client.get(books_url)
    templates_used = [t.name for t in response.templates]

    assert CHANGEFORM_TEMPLATES["carousel"] in templates_used

    response = admin_client.get(users_url)
    templates_used = [t.name for t in response.templates]

    assert CHANGEFORM_TEMPLATES["vertical_tabs"] in templates_used


@pytest.mark.django_db
def test_changeform_template_default(admin_client):
    """
    The horizontal_tabs template is used by default
    """
    book = BookFactory()

    books_url = reverse("admin:books_book_change", args=(book.pk,))

    response = admin_client.get(books_url)
    templates_used = [t.name for t in response.templates]

    assert CHANGEFORM_TEMPLATES["horizontal_tabs"] in templates_used


@pytest.mark.django_db
@mock.patch.object(BookAdmin, "fieldsets", None)
@mock.patch.object(BookAdmin, "inlines", [])
def test_changeform_single(admin_client):
    """
    The single template is used when the modeladmin has no fieldsets, or inlines
    """
    book = BookFactory()

    books_url = reverse("admin:books_book_change", args=(book.pk,))

    response = admin_client.get(books_url)

    templates_used = [t.name for t in response.templates]

    assert CHANGEFORM_TEMPLATES["single"] in templates_used
