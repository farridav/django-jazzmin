import pytest
from django.urls import reverse

from .test_app.library.factories import BookFactory, UserFactory
from .utils import parse_sidemenu


@pytest.mark.django_db
def test_no_delete_permission(client):
    """
    When our user has no delete permission, they dont see things they are not supposed to
    """
    user = UserFactory(permissions=["books.view_book"])
    book = BookFactory()

    url = reverse("admin:books_book_change", args=(book.pk,))
    delete_url = reverse("admin:books_book_delete", args=(book.pk,))
    client.force_login(user)

    response = client.get(url)
    assert delete_url not in response.content.decode()


@pytest.mark.django_db
def test_no_add_permission(client):
    """
    When our user has no add permission, they dont see things they are not supposed to
    """
    user = UserFactory(permissions=["books.view_book"])
    url = reverse("admin:books_book_changelist")
    add_url = reverse("admin:books_book_add")

    client.force_login(user)
    response = client.get(url)

    assert add_url not in response.content.decode()


@pytest.mark.django_db
def test_delete_but_no_view_permission(client):
    """
    When our user has delete but no view/change permission, menu items render out, but with no links

    As in Plain old Django Admin
    """
    user = UserFactory(permissions=["books.delete_book"])

    url = reverse("admin:index")
    client.force_login(user)

    response = client.get(url)
    assert parse_sidemenu(response) == {"Global": ["/en/admin/"], "Books": [None]}


@pytest.mark.django_db
def test_no_permission(client):
    """
    When our user has no permissions at all, they see no menu or dashboard

    As in Plain old Django Admin
    """
    user = UserFactory(permissions=[])

    url = reverse("admin:index")
    client.force_login(user)

    response = client.get(url)
    assert parse_sidemenu(response) == {"Global": ["/en/admin/"]}
