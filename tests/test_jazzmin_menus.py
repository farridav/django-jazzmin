import pytest
from django.urls import reverse

from .test_app.library.factories import UserFactory
from .utils import parse_sidemenu, parse_topmenu, parse_usermenu


@pytest.mark.django_db
def test_side_menu(admin_client, custom_jazzmin_settings):
    """
    All menu tweaking settings work as expected
    """
    url = reverse("admin:index")

    response = admin_client.get(url)

    assert parse_sidemenu(response) == {
        "Administration": ["/en/admin/admin/logentry/"],
        "Authentication and Authorization": [
            "/en/admin/auth/group/",
            "/en/admin/auth/user/",
        ],
        "Books": [
            "/en/admin/books/author/",
            "/en/admin/books/book/",
            "/en/admin/books/genre/",
        ],
        "Global": ["/en/admin/"],
        "Loans": [
            "/make_messages/",
            "/en/admin/loans/bookloan/",
            "/en/admin/loans/library/",
            "/en/admin/loans/bookloan/custom_view",
        ],
    }

    custom_jazzmin_settings["hide_models"] = ["auth.user"]
    response = admin_client.get(url)

    assert parse_sidemenu(response) == {
        "Global": ["/en/admin/"],
        "Authentication and Authorization": ["/en/admin/auth/group/"],
        "Books": [
            "/en/admin/books/author/",
            "/en/admin/books/book/",
            "/en/admin/books/genre/",
        ],
        "Loans": [
            "/make_messages/",
            "/en/admin/loans/bookloan/",
            "/en/admin/loans/library/",
            "/en/admin/loans/bookloan/custom_view",
        ],
        "Administration": ["/en/admin/admin/logentry/"],
    }


@pytest.mark.django_db
def test_permissions_on_custom_links(client, custom_jazzmin_settings):
    """
    we honour permissions for the rendering of custom links
    """
    user = UserFactory()
    user2 = UserFactory(permissions=("books.view_book",))

    url = reverse("admin:index")

    custom_jazzmin_settings["custom_links"] = {
        "books": [
            {
                "name": "Make Messages",
                "url": "make_messages",
                "icon": "fa-comments",
                "permissions": ["books.view_book"],
            }
        ]
    }

    client.force_login(user)
    response = client.get(url)
    assert parse_sidemenu(response) == {"Global": ["/en/admin/"]}

    client.force_login(user2)
    response = client.get(url)
    assert parse_sidemenu(response) == {
        "Global": ["/en/admin/"],
        "Books": ["/make_messages/", "/en/admin/books/book/"],
    }


@pytest.mark.django_db
def test_top_menu(admin_client, custom_jazzmin_settings):
    """
    Top menu renders out as expected
    """
    url = reverse("admin:index")

    custom_jazzmin_settings["topmenu_links"] = [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {
            "name": "Support",
            "url": "https://github.com/farridav/django-jazzmin/issues",
            "new_window": True,
        },
        {"model": "auth.User"},
        {"app": "books"},
    ]

    response = admin_client.get(url)

    assert parse_topmenu(response) == [
        {"name": "Home", "link": "/en/admin/"},
        {
            "name": "Support",
            "link": "https://github.com/farridav/django-jazzmin/issues",
        },
        {"name": "Users", "link": "/en/admin/auth/user/"},
        {
            "name": "Books",
            "link": "#",
            "children": [
                {"name": "Genres", "link": "/en/admin/books/genre/"},
                {"name": "Books", "link": "/en/admin/books/book/"},
                {"name": "Authors", "link": "/en/admin/books/author/"},
            ],
        },
    ]


@pytest.mark.django_db
def test_user_menu(admin_user, client, custom_jazzmin_settings):
    """
    The User menu renders out as expected
    """
    url = reverse("admin:index")

    custom_jazzmin_settings["usermenu_links"] = [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {
            "name": "Support",
            "url": "https://github.com/farridav/django-jazzmin/issues",
            "new_window": True,
        },
        {"model": "auth.User"},
    ]

    client.force_login(admin_user)
    response = client.get(url)

    assert parse_usermenu(response) == [
        {"link": "/en/admin/password_change/", "name": "Change password"},
        {"link": "/en/admin/logout/", "name": "Log out"},
        {"link": "/en/admin/", "name": "Home"},
        {
            "link": "https://github.com/farridav/django-jazzmin/issues",
            "name": "Support",
        },
        {"link": "/en/admin/auth/user/", "name": "Users"},
        {
            "link": "/en/admin/auth/user/{}/change/".format(admin_user.pk),
            "name": "See Profile",
        },
    ]
