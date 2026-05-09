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


@pytest.mark.django_db
def test_is_visible_on_custom_links(client, custom_jazzmin_settings):
    """
    is_visible callable controls visibility of custom side menu links.
    The callable receives the request object for access to user, path, session, etc.
    """
    from .test_app.library.factories import GroupFactory

    editors_group = GroupFactory(name="editors")
    user_in_group = UserFactory(groups=(editors_group,), permissions=("books.view_book",))
    user_not_in_group = UserFactory(permissions=("books.view_book",))

    url = reverse("admin:index")

    custom_jazzmin_settings["custom_links"] = {
        "books": [
            {
                "name": "Editor Dashboard",
                "url": "make_messages",
                "icon": "fa-comments",
                "is_visible": lambda r: r.user.groups.filter(name="editors").exists(),
            }
        ]
    }

    # User in group should see the link
    client.force_login(user_in_group)
    menu = parse_sidemenu(client.get(url))
    assert "/make_messages/" in menu.get("Books", [])

    # User not in group should NOT see the link
    client.force_login(user_not_in_group)
    menu = parse_sidemenu(client.get(url))
    assert "/make_messages/" not in menu.get("Books", [])


@pytest.mark.django_db
def test_is_visible_on_topmenu(client, custom_jazzmin_settings):
    """
    is_visible callable controls visibility of top menu links.
    """
    superuser = UserFactory(is_superuser=True)
    regular_user = UserFactory()

    url = reverse("admin:index")

    custom_jazzmin_settings["topmenu_links"] = [
        {"name": "Admin Only", "url": "admin:index", "is_visible": lambda r: r.user.is_superuser},
        {"name": "Public Link", "url": "admin:index"},
    ]

    # Superuser should see both links
    client.force_login(superuser)
    assert parse_topmenu(client.get(url)) == [
        {"name": "Admin Only", "link": "/en/admin/"},
        {"name": "Public Link", "link": "/en/admin/"},
    ]

    # Regular user should see only the public link
    client.force_login(regular_user)
    assert parse_topmenu(client.get(url)) == [
        {"name": "Public Link", "link": "/en/admin/"},
    ]


@pytest.mark.django_db
def test_is_visible_on_usermenu(client, custom_jazzmin_settings):
    """
    is_visible callable controls visibility of user menu links.
    """
    superuser = UserFactory(is_superuser=True)
    regular_user = UserFactory()

    url = reverse("admin:index")

    custom_jazzmin_settings["usermenu_links"] = [
        {"name": "Admin Settings", "url": "admin:index", "is_visible": lambda r: r.user.is_superuser},
        {"name": "My Profile", "url": "admin:index"},
    ]

    # Superuser should see both links
    client.force_login(superuser)
    menu = parse_usermenu(client.get(url))
    assert {"name": "Admin Settings", "link": "/en/admin/"} in menu
    assert {"name": "My Profile", "link": "/en/admin/"} in menu

    # Regular user should see only the profile link
    client.force_login(regular_user)
    menu = parse_usermenu(client.get(url))
    assert {"name": "Admin Settings", "link": "/en/admin/"} not in menu
    assert {"name": "My Profile", "link": "/en/admin/"} in menu


@pytest.mark.django_db
def test_is_visible_with_request_path(admin_client, custom_jazzmin_settings):
    """
    is_visible can use request.path for context-aware menu visibility.
    """
    custom_jazzmin_settings["topmenu_links"] = [
        {"name": "Books Context Menu", "url": "admin:index", "is_visible": lambda r: "/books/" in r.path},
        {"name": "Always Visible", "url": "admin:index"},
    ]

    # On admin index - should not see the books-specific link
    assert parse_topmenu(admin_client.get(reverse("admin:index"))) == [
        {"name": "Always Visible", "link": "/en/admin/"},
    ]

    # On books page - should see the books-specific link
    assert parse_topmenu(admin_client.get(reverse("admin:books_book_changelist"))) == [
        {"name": "Books Context Menu", "link": "/en/admin/"},
        {"name": "Always Visible", "link": "/en/admin/"},
    ]


@pytest.mark.django_db
def test_is_visible_combined_with_permissions(client, custom_jazzmin_settings):
    """
    is_visible works together with permissions - both conditions must be met.
    """
    from .test_app.library.factories import GroupFactory

    editors_group = GroupFactory(name="editors")
    # User with both permission AND group
    user_with_both = UserFactory(groups=(editors_group,), permissions=("books.view_book", "books.change_book"))
    # User with permission but NOT in group
    user_with_only_perm = UserFactory(permissions=("books.view_book", "books.change_book"))
    # User in group but missing permission
    user_with_only_group = UserFactory(groups=(editors_group,), permissions=("books.view_book",))

    url = reverse("admin:index")

    custom_jazzmin_settings["custom_links"] = {
        "books": [
            {
                "name": "Editor Tools",
                "url": "make_messages",
                "permissions": ["books.change_book"],
                "is_visible": lambda r: r.user.groups.filter(name="editors").exists(),
            }
        ]
    }

    # User with both permission and group should see the link
    client.force_login(user_with_both)
    assert "/make_messages/" in parse_sidemenu(client.get(url)).get("Books", [])

    # User with only permission (not in group) should NOT see the link
    client.force_login(user_with_only_perm)
    assert "/make_messages/" not in parse_sidemenu(client.get(url)).get("Books", [])

    # User in group but missing permission should NOT see the link
    client.force_login(user_with_only_group)
    assert "/make_messages/" not in parse_sidemenu(client.get(url)).get("Books", [])


@pytest.mark.django_db
def test_is_visible_with_or_logic(client, custom_jazzmin_settings):
    """
    is_visible can implement OR logic between multiple groups.
    """
    from .test_app.library.factories import GroupFactory

    editors_group = GroupFactory(name="editors")
    managers_group = GroupFactory(name="managers")
    user_editor = UserFactory(groups=(editors_group,), permissions=("books.view_book",))
    user_manager = UserFactory(groups=(managers_group,), permissions=("books.view_book",))
    user_neither = UserFactory(permissions=("books.view_book",))

    url = reverse("admin:index")

    custom_jazzmin_settings["custom_links"] = {
        "books": [
            {
                "name": "Staff Tools",
                "url": "make_messages",
                "is_visible": lambda r: r.user.groups.filter(name__in=["editors", "managers"]).exists(),
            }
        ]
    }

    # Editor should see the link
    client.force_login(user_editor)
    assert "/make_messages/" in parse_sidemenu(client.get(url)).get("Books", [])

    # Manager should see the link
    client.force_login(user_manager)
    assert "/make_messages/" in parse_sidemenu(client.get(url)).get("Books", [])

    # User in neither group should NOT see the link
    client.force_login(user_neither)
    assert "/make_messages/" not in parse_sidemenu(client.get(url)).get("Books", [])
