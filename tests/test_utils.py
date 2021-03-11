from unittest.mock import patch, MagicMock, Mock

import pytest
from django.db.models.functions import Upper
from django.urls import reverse

from jazzmin.utils import (
    order_with_respect_to,
    get_admin_url,
    get_custom_url,
    get_model_meta,
    get_app_admin_urls,
    get_view_permissions,
)
from .test_app.library.factories import BookFactory, UserFactory
from .test_app.library.books.models import Book


def test_order_with_respect_to():
    """
    When we ask for ordering, we get it as expected
    """

    def apps(*args):
        return [{"app_label": x} for x in args]

    original_list = apps("b", "c", "a")

    assert order_with_respect_to(original_list, ["c", "b"], getter=lambda x: x["app_label"]) == apps("c", "b", "a")
    assert order_with_respect_to(original_list, ["nothing"], getter=lambda x: x["app_label"]) == original_list
    assert order_with_respect_to(original_list, ["a"], getter=lambda x: x["app_label"])[0]["app_label"] == "a"
    assert order_with_respect_to([1, 2, 3], [3, 2, 1]) == [3, 2, 1]
    assert order_with_respect_to([1, 2, 3], [3]) == [3, 1, 2]
    assert order_with_respect_to(["morty", "pickle", "rick"], ["pickle", "morty"]) == [
        "pickle",
        "morty",
        "rick",
    ]


@pytest.mark.django_db
def test_get_admin_url(admin_user):
    """
    We can get admin urls for Model classes, instances, or app.model strings
    """
    book = BookFactory()

    assert get_admin_url(book) == reverse("admin:books_book_change", args=(book.pk,))
    assert get_admin_url(Book) == reverse("admin:books_book_changelist")
    assert get_admin_url(Book, q="test") == reverse("admin:books_book_changelist") + "?q=test"
    assert get_admin_url("books.Book") == reverse("admin:books_book_changelist")
    with patch("jazzmin.utils.reverse") as mock_reverse:
        get_admin_url("Books.Book")
        mock_reverse.assert_called_once_with("admin:Books_book_changelist", current_app="admin")
    assert get_admin_url("cheese:bad_pattern") == "#"
    assert get_admin_url("fake_app.fake_model") == "#"
    assert get_admin_url(1) == "#"


def test_get_custom_url():
    """
    We handle urls that can be reversed, and that cant, and external links
    """
    assert get_custom_url("http://somedomain.com") == "http://somedomain.com"
    assert get_custom_url("/relative/path") == "/relative/path"
    assert get_custom_url("admin:books_book_changelist") == "/en/admin/books/book/"


@pytest.mark.django_db
def test_get_model_meta(admin_user):
    """
    We can fetch model meta
    """
    assert get_model_meta("auth.user") == admin_user._meta
    assert get_model_meta("books.book") == Book._meta
    assert get_model_meta("nothing") is None
    assert get_model_meta("nothing.nothing") is None


@pytest.mark.django_db
def test_get_app_admin_urls():
    """
    We can get all the admin urls for an app
    """
    assert get_app_admin_urls("books") == [
        {"url": "/en/admin/books/genre/", "model": "books.genre", "name": "Genres"},
        {"url": "/en/admin/books/book/", "model": "books.book", "name": "Books"},
        {"url": "/en/admin/books/author/", "model": "books.author", "name": "Authors"},
    ]

    assert get_app_admin_urls("nothing") == []


@pytest.mark.django_db
def test_get_model_permissions():
    """
    We can create the correct model permissions from user permissions
    """
    user = UserFactory(permissions=("books.view_book", "books.view_author"))

    assert get_view_permissions(user) == {"books.book", "books.author"}

    # test for camel cased app names
    user = MagicMock()
    user.get_all_permissions = Mock(return_value={"BookShelf.view_author", "BookShelf.view_book"})

    assert get_view_permissions(user) == {"BookShelf.book", "BookShelf.author"}


@pytest.mark.django_db
def test_get_model_permissions_lowercased():
    """
    When our permissions are upper cased (we had an app with an upper case letter) we still get user perms in lower case
    """
    user = UserFactory(permissions=("books.view_book", "books.view_author"))
    user.user_permissions.update(codename=Upper("codename"))

    assert get_view_permissions(user) == {"books.book", "books.author"}
