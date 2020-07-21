import pytest
from django.urls import reverse

from .utils import parse_sidemenu, user_with_permissions, parse_topmenu, parse_usermenu, override_jazzmin_settings


@pytest.mark.django_db
def test_side_menu(admin_client, settings):
    """
    All menu tweaking settings work as expected
    """
    url = reverse("admin:index")

    response = admin_client.get(url)

    assert parse_sidemenu(response) == {
        "Global": ["/admin/"],
        "Polls": [
            "/admin/polls/allfields/",
            "/admin/polls/campaign/",
            "/admin/polls/cheese/",
            "/admin/polls/choice/",
            "/admin/polls/poll/",
            "/admin/polls/vote/",
            "/make_messages/",
        ],
        "Administration": ["/admin/admin/logentry/"],
        "Authentication and Authorization": ["/admin/auth/group/", "/admin/auth/user/"],
    }

    settings.JAZZMIN_SETTINGS = override_jazzmin_settings(hide_models=["auth.user"])
    response = admin_client.get(url)

    assert parse_sidemenu(response) == {
        "Global": ["/admin/"],
        "Polls": [
            "/admin/polls/allfields/",
            "/admin/polls/campaign/",
            "/admin/polls/cheese/",
            "/admin/polls/choice/",
            "/admin/polls/poll/",
            "/admin/polls/vote/",
            "/make_messages/",
        ],
        "Administration": ["/admin/admin/logentry/"],
        "Authentication and Authorization": ["/admin/auth/group/"],
    }


@pytest.mark.django_db
def test_permissions_on_custom_links(client, settings):
    """
    we honour permissions for the rendering of custom links
    """
    user = user_with_permissions()
    user2 = user_with_permissions("polls.view_poll")

    url = reverse("admin:index")

    settings.JAZZMIN_SETTINGS = override_jazzmin_settings(custom_links={
        "polls": [
            {"name": "Make Messages", "url": "make_messages", "icon": "fa-comments", "permissions": ["polls.view_poll"]}
        ]
    })

    client.force_login(user)
    response = client.get(url)
    assert parse_sidemenu(response) == {"Global": ["/admin/"]}

    client.force_login(user2)
    response = client.get(url)
    assert parse_sidemenu(response) == {"Global": ["/admin/"], "Polls": ["/admin/polls/poll/", "/make_messages/"]}


@pytest.mark.django_db
def test_top_menu(admin_client, settings):
    """
    Top menu renders out as expected
    """
    url = reverse("admin:index")

    settings.JAZZMIN_SETTINGS = override_jazzmin_settings(topmenu_links=[
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "auth.User"},
        {"app": "polls"},
    ])

    response = admin_client.get(url)

    assert parse_topmenu(response) == [
        {"name": "Home", "link": "/admin/"},
        {"name": "Support", "link": "https://github.com/farridav/django-jazzmin/issues"},
        {"name": "Users", "link": "/admin/auth/user/"},
        {
            "name": "Polls",
            "link": "#",
            "children": [
                {"name": "Polls", "link": reverse("admin:polls_poll_changelist")},
                {"name": "Choices", "link": reverse("admin:polls_choice_changelist")},
                {"name": "Votes", "link": reverse("admin:polls_vote_changelist")},
                {"name": "Cheeses", "link": reverse("admin:polls_cheese_changelist")},
                {"name": "Campaigns", "link": reverse("admin:polls_campaign_changelist")},
                {"name": "Allfields", "link": reverse("admin:polls_allfields_changelist")},
            ],
        },
    ]


@pytest.mark.django_db
def test_user_menu(admin_user, client, settings):
    """
    The User menu renders out as expected
    """
    url = reverse("admin:index")

    settings.JAZZMIN_SETTINGS = override_jazzmin_settings(usermenu_links=[
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "auth.User"},
    ])

    client.force_login(admin_user)
    response = client.get(url)

    assert parse_usermenu(response) == [
        {"link": "/admin/password_change/", "name": "Change password"},
        {"link": "/admin/logout/", "name": "Log out"},
        {"link": "/admin/", "name": "Home"},
        {"link": "https://github.com/farridav/django-jazzmin/issues", "name": "Support"},
        {"link": "/admin/auth/user/", "name": "Users"},
        {"link": "/admin/auth/user/{}/change/".format(admin_user.pk), "name": "See Profile"},
    ]
