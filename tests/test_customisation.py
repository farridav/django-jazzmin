import pytest
from bs4 import BeautifulSoup
from django.urls import reverse
from jazzmin.settings import CHANGEFORM_TEMPLATES
from jazzmin.templatetags.jazzmin import get_sections

from .test_app.library.books.admin import BookAdmin
from .test_app.library.factories import BookFactory, UserFactory


@pytest.mark.django_db
def test_update_site_logo(admin_client, custom_jazzmin_settings):
    """
    We can add a site logo, and it renders out
    """
    url = reverse("admin:index")

    custom_jazzmin_settings["site_logo"] = "books/img/logo.png"
    response = admin_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    assert soup.find("a", class_="brand-link").find("img")["src"] == "/static/books/img/logo.png"


@pytest.mark.django_db
def test_update_login_logo(client, custom_jazzmin_settings):
    """
    We can add a login logo, and it renders out
    """
    url = reverse("admin:login")

    custom_jazzmin_settings["login_logo"] = "books/img/logo-login.png"
    response = client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    assert soup.find("div", class_="login-logo").find("img")["src"] == "/static/books/img/logo-login.png"


@pytest.mark.django_db
@pytest.mark.parametrize("config_value,template", [(k, v) for k, v in CHANGEFORM_TEMPLATES.items()])
def test_changeform_templates(config_value, template, admin_client, custom_jazzmin_settings):
    """
    All changeform config values use the correct templates
    """
    custom_jazzmin_settings["changeform_format"] = config_value
    book = BookFactory()
    url = reverse("admin:books_book_change", args=(book.pk,))

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]

    assert template in templates_used


@pytest.mark.django_db
def test_changeform_template_override(admin_client, custom_jazzmin_settings):
    """
    We can set a global template, and override it per model
    """
    custom_jazzmin_settings.update(
        {"changeform_format": "vertical_tabs", "changeform_format_overrides": {"books.book": "carousel"}}
    )

    user = UserFactory()
    book = BookFactory()

    books_url = reverse("admin:books_book_change", args=(book.pk,))
    users_url = reverse("admin:auth_user_change", args=(user.pk,))

    response = admin_client.get(books_url)
    templates_used = [t.name for t in response.templates]

    assert CHANGEFORM_TEMPLATES["carousel"] in templates_used

    response = admin_client.get(users_url)
    templates_used = [t.name for t in response.templates]

    assert CHANGEFORM_TEMPLATES["vertical_tabs"] in templates_used


@pytest.mark.django_db
def test_changeform_template_default(admin_client, custom_jazzmin_settings):
    """
    The horizontal_tabs template is used by default
    """
    assert custom_jazzmin_settings["changeform_format"] == "horizontal_tabs"
    book = BookFactory()

    books_url = reverse("admin:books_book_change", args=(book.pk,))

    response = admin_client.get(books_url)
    templates_used = [t.name for t in response.templates]

    assert CHANGEFORM_TEMPLATES["horizontal_tabs"] in templates_used


@pytest.mark.django_db
def test_changeform_single(admin_client, monkeypatch):
    """
    The single template is used when the modeladmin has no fieldsets, or inlines
    """
    book = BookFactory()
    books_url = reverse("admin:books_book_change", args=(book.pk,))
    monkeypatch.setattr(BookAdmin, "fieldsets", None)
    monkeypatch.setattr(BookAdmin, "inlines", [])

    response = admin_client.get(books_url)

    templates_used = [t.name for t in response.templates]
    assert CHANGEFORM_TEMPLATES["single"] in templates_used


@pytest.mark.django_db
@pytest.mark.parametrize("order", [("Book loans", "general", "other"), ("other", "Book loans", "general")])
def test_changeform_section_ordering(change_form_context, order):
    """
    We respect the given order for sections
    """
    admin_form = change_form_context["adminform"]
    inline_formsets = change_form_context["inline_admin_formsets"]

    admin_form.model_admin.jazzmin_section_order = order
    fieldsets = get_sections(admin_form, inline_formsets)

    assert tuple(x.name for x in fieldsets) == order
