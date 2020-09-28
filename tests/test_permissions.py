import pytest
from django.urls import reverse

from tests.test_app.polls.models import Poll
from tests.utils import user_with_permissions, parse_sidemenu


@pytest.mark.django_db
def test_no_delete_permission(client):
    """
    When our user has no delete permission, they dont see things they are not supposed to
    """
    user = user_with_permissions("polls.view_poll")
    poll = Poll.objects.create(owner=user, text="question")

    url = reverse("admin:polls_poll_change", args=(poll.pk,))
    delete_url = reverse("admin:polls_poll_delete", args=(poll.pk,))
    client.force_login(user)

    response = client.get(url)
    assert delete_url not in response.content.decode()


@pytest.mark.django_db
def test_no_add_permission(client):
    """
    When our user has no add permission, they dont see things they are not supposed to
    """
    user = user_with_permissions("polls.view_poll")
    url = reverse("admin:polls_poll_changelist")
    add_url = reverse("admin:polls_poll_add")

    client.force_login(user)
    response = client.get(url)

    assert add_url not in response.content.decode()


@pytest.mark.django_db
def test_delete_but_no_view_permission(client):
    """
    When our user has delete but no view/change permission, menu items render out, but with no links

    As in Plain old Django Admin
    """
    user = user_with_permissions("polls.delete_poll")

    url = reverse("admin:index")
    client.force_login(user)

    response = client.get(url)
    assert parse_sidemenu(response) == {"Global": ["/admin/"], "Polls": [None]}


@pytest.mark.django_db
def test_no_permission(client):
    """
    When our user has no permissions at all, they see no menu or dashboard

    As in Plain old Django Admin
    """
    user = user_with_permissions()

    url = reverse("admin:index")
    client.force_login(user)

    response = client.get(url)
    assert parse_sidemenu(response) == {"Global": ["/admin/"]}
