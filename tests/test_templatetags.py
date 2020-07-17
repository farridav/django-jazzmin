import pytest
from django.contrib.admin.models import LogEntry, CHANGE

from jazzmin.templatetags import jazzmin


@pytest.mark.django_db
def test_app_is_installed(settings):
    """
    Returns True if an app is under INSTALLED_APPS, False otherwise
    """
    app = "test_app"

    assert jazzmin.app_is_installed(app) is False

    settings.INSTALLED_APPS.append(app)

    assert jazzmin.app_is_installed(app) is True


@pytest.mark.django_db
def test_action_message_to_list(admin_user):
    """
    We can generate a list of messages from a log entry object
    """
    message = (
        '[{"changed": {"fields": ["Owner", "Text", "Pub date", "Active"]}}, '
        '{"added": {"name": "choice", "object": "More random choices"}}, '
        '{"deleted": {"name": "choice", "object": "Person serious choose tea"}}]'
    )
    log_entry = LogEntry.objects.create(user=admin_user, action_flag=CHANGE, change_message=message)
    assert jazzmin.action_message_to_list(log_entry) == [
        "Changed Owner, Text, Pub date and Active.",
        "Added choice “More random choices”.",
        "Deleted choice “Person serious choose tea”.",
    ]


def test_get_action_icon():
    """
    Returns icon depending on action being added, changed or deleted
    """
    add_message = "Added cheese option"
    change_message = "Changed cheese option"
    delete_message = "Deleted cheese option"

    assert jazzmin.get_action_icon(add_message) == "plus-circle"
    assert jazzmin.get_action_icon(change_message) == "edit"
    assert jazzmin.get_action_icon(delete_message) == "trash"


def test_get_action_color():
    """
    Returns color depending on action being added, changed or deleted
    """
    add_message = "Added cheese option"
    change_message = "Changed cheese option"
    delete_message = "Deleted cheese option"

    assert jazzmin.get_action_color(add_message) == "success"
    assert jazzmin.get_action_color(change_message) == "blue"
    assert jazzmin.get_action_color(delete_message) == "danger"


def test_style_bold_first_word():
    """
    Adds <strong> HTML element wrapping first word given a sentence
    """
    message = "The bomb has been planted"

    assert jazzmin.style_bold_first_word(message) == "<strong>The</strong> bomb has been planted"
