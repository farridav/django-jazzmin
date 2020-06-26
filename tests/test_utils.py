import pytest
from django.urls import reverse

from jazzmin.utils import (
    order_with_respect_to,
    get_admin_url,
    get_custom_url,
    get_model_meta,
    get_app_admin_urls,
    get_view_permissions,
)
from tests.test_app.polls.models import Poll
from tests.utils import user_with_permissions


def test_order_with_respect_to():
    """
    When we ask for ordering, we get it as expected
    """

    def apps(*args):
        return [{"app_label": x} for x in args]

    original_list = apps("b", "c", "a")

    assert order_with_respect_to(original_list, ["c", "b"]) == apps("c", "b", "a")
    assert order_with_respect_to(original_list, ["nothing"]) == original_list
    assert order_with_respect_to(original_list, ["a"])[0]["app_label"] == "a"


@pytest.mark.django_db
def test_get_admin_url(admin_user):
    """
    We can get admin urls for Model classes, instances, or app.model strings
    """
    poll = Poll.objects.create(owner=admin_user, text="question")

    assert get_admin_url(poll) == reverse("admin:polls_poll_change", args=(poll.pk,))
    assert get_admin_url(Poll) == reverse("admin:polls_poll_changelist")
    assert get_admin_url(Poll, q="test") == reverse("admin:polls_poll_changelist") + "?q=test"
    assert get_admin_url("polls.Poll") == reverse("admin:polls_poll_changelist")
    assert get_admin_url("cheese:bad_pattern") == "#"
    assert get_admin_url("fake_app.fake_model") == "#"
    assert get_admin_url(1) == "#"


def test_get_custom_url():
    """
    We handle urls that can be reversed, and that cant, and external links
    """
    assert get_custom_url("http://somedomain.com") == "http://somedomain.com"
    assert get_custom_url("/relative/path") == "/relative/path"
    assert get_custom_url("admin:polls_poll_changelist") == "/admin/polls/poll/"


@pytest.mark.django_db
def test_get_model_meta(admin_user):
    """
    We can fetch model meta
    """
    assert get_model_meta("auth.user") == admin_user._meta
    assert get_model_meta("polls.poll") == Poll._meta
    assert get_model_meta("nothing") is None
    assert get_model_meta("nothing.nothing") is None


@pytest.mark.django_db
def test_get_app_admin_urls():
    """
    We can get all the admin urls for an app
    """
    assert get_app_admin_urls("polls") == [
        {"model": "polls.poll", "name": "Polls", "url": reverse("admin:polls_poll_changelist")},
        {"model": "polls.choice", "name": "Choices", "url": reverse("admin:polls_choice_changelist")},
        {"model": "polls.vote", "name": "Votes", "url": reverse("admin:polls_vote_changelist")},
        {"model": "polls.cheese", "name": "Cheeses", "url": reverse("admin:polls_cheese_changelist")},
        {"model": "polls.campaign", "name": "Campaigns", "url": reverse("admin:polls_campaign_changelist")},
    ]

    assert get_app_admin_urls("nothing") == []


@pytest.mark.django_db
def test_get_model_permissions():
    """
    We can create the correct model permissions from user permissions
    """

    user = user_with_permissions("polls.view_poll", "polls.view_choice")

    assert get_view_permissions(user) == {"polls.poll", "polls.choice"}
