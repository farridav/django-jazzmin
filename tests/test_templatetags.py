import json
from unittest.mock import MagicMock, NonCallableMock
import copy

import pytest
from django.contrib.admin.models import CHANGE, LogEntry
from django.template import Context
from django.contrib.auth import get_user_model

from jazzmin.templatetags import jazzmin

User = get_user_model()


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
    message = [
        {"changed": {"fields": ["Owner", "Text", "Pub date", "Active"]}},
        {"added": {"name": "choice", "object": "More random choices"}},
        {"deleted": {"name": "choice", "object": "Person serious choose tea"}},
    ]
    log_entry = LogEntry.objects.create(user=admin_user, action_flag=CHANGE, change_message=json.dumps(message))
    assert jazzmin.action_message_to_list(log_entry) == [
        {"msg": "Changed Owner, Text, Pub date and Active.", "icon": "edit", "colour": "blue"},
        {"msg": "Added choice “More random choices”.", "icon": "plus-circle", "colour": "success"},
        {"msg": "Deleted “Person serious choose tea”.", "icon": "trash", "colour": "danger"},
    ]


def test_style_bold_first_word():
    """
    Adds <strong> HTML element wrapping first word given a sentence
    """
    message = "The bomb has been planted"

    assert jazzmin.style_bold_first_word(message) == "<strong>The</strong> bomb has been planted"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "case,test_input,field,expected,log",
    [
        (1, MagicMock(avatar="image.jpg"), "avatar", "image.jpg", None),
        (2, MagicMock(avatar="image.jpg"), lambda u: u.avatar, "image.jpg", None),
        (3, MagicMock(avatar=MagicMock(url="image.jpg")), "avatar", "image.jpg", None),
        # Properly set file field but empty (no image uploaded)
        (
            4,
            MagicMock(avatar=MagicMock(__bool__=lambda x: False)),
            "avatar",
            "/static/vendor/adminlte/img/user2-160x160.jpg",
            None,
        ),
        # No avatar field set
        (
            5,
            MagicMock(
                avatar="image.jpg",
            ),
            None,
            "/static/vendor/adminlte/img/user2-160x160.jpg",
            None,
        ),
        # No proper avatar field set
        (
            6,
            MagicMock(avatar=NonCallableMock(spec_set=["__bool__"], __bool__=lambda x: True)),
            "avatar",
            "/static/vendor/adminlte/img/user2-160x160.jpg",
            "Avatar field must be",
        ),
    ],
)
def test_get_user_avatar(case, test_input, field, expected, log, custom_jazzmin_settings, caplog):
    """
    We can specify the name of a charfield or imagefield on our user model, or a callable that receives our user
    """
    custom_jazzmin_settings["user_avatar"] = field
    assert jazzmin.get_user_avatar(test_input) == expected
    if log:
        assert log in caplog.text
    else:
        assert not caplog.text


@pytest.mark.django_db
def test_get_side_menu_without_user():
    """Test that side menu returns empty list when no user in context"""
    context = Context({})
    menu = jazzmin.get_side_menu(context)
    assert menu == []


@pytest.mark.django_db
def test_get_side_menu_with_user(admin_user, custom_jazzmin_settings):
    """Test that side menu returns apps when user is in context"""

    context = Context(
        {
            "user": admin_user,
            "available_apps": [
                {
                    "name": "Test App",
                    "app_label": "test_app",
                    "app_url": "/admin/test_app",
                    "has_module_perms": True,
                    "models": [
                        {
                            "name": "Test Model",
                            "object_name": "TestModel",
                            "admin_url": "/admin/test_app/testmodel",
                            "view_only": False,
                        }
                    ],
                }
            ],
        }
    )

    menu = jazzmin.get_side_menu(context)

    assert menu == [
        {
            "name": "Test App",
            "app_label": "test_app",
            "app_url": "/admin/test_app",
            "has_module_perms": True,
            "icon": "fas fa-chevron-circle-right",
            "models": [
                {
                    "name": "Test Model",
                    "object_name": "TestModel",
                    "admin_url": "/admin/test_app/testmodel",
                    "view_only": False,
                    "url": "/admin/test_app/testmodel",
                    "model_str": "test_app.testmodel",
                    "icon": "fas fa-circle",
                }
            ],
        }
    ]


@pytest.mark.django_db
def test_get_side_menu_with_hidden_app(admin_user, custom_jazzmin_settings):
    """Test that hidden apps are not included in the menu"""
    custom_jazzmin_settings["hide_apps"] = ["hidden_app"]

    context = Context(
        {
            "user": admin_user,
            "available_apps": [
                {
                    "name": "Hidden App",
                    "app_label": "hidden_app",
                    "app_url": "/admin/hidden_app",
                    "has_module_perms": True,
                    "models": [],
                }
            ],
        }
    )

    menu = jazzmin.get_side_menu(context)
    assert len(menu) == 0


@pytest.mark.django_db
def test_get_side_menu_with_custom_links(admin_user, custom_jazzmin_settings):
    """Test that custom links are added to the menu"""
    custom_jazzmin_settings["custom_links"] = {"custom_app": [{"name": "Custom Link", "url": "http://example.com"}]}

    context = Context({"user": admin_user, "available_apps": []})

    menu = jazzmin.get_side_menu(context)

    assert menu == [
        {
            "name": "custom_app",
            "app_label": "custom_app",
            "app_url": "#",
            "has_module_perms": True,
            "icon": "fas fa-chevron-circle-right",
            "models": [
                {
                    "name": "Custom Link",
                    "url": "http://example.com",
                    "children": None,
                    "new_window": False,
                    "icon": None,
                }
            ],
        }
    ]


@pytest.mark.django_db
def test_get_side_menu_ordering(admin_user, custom_jazzmin_settings):
    """Test that menu items are ordered correctly"""
    custom_jazzmin_settings["order_with_respect_to"] = ["first_app", "second_app"]

    context = Context(
        {
            "user": admin_user,
            "available_apps": [
                {
                    "name": "Second App",
                    "app_label": "second_app",
                    "app_url": "/admin/second_app",
                    "has_module_perms": True,
                    "models": [
                        {
                            "name": "Test Model 2",
                            "object_name": "TestModel 2",
                            "admin_url": "/admin/test_app/testmodel2",
                            "view_only": False,
                        }
                    ],
                },
                {
                    "name": "First App",
                    "app_label": "first_app",
                    "app_url": "/admin/first_app",
                    "has_module_perms": True,
                    "models": [
                        {
                            "name": "Test Model 1",
                            "object_name": "TestModel 1",
                            "admin_url": "/admin/test_app/testmodel1",
                            "view_only": False,
                        }
                    ],
                },
            ],
        }
    )

    menu = jazzmin.get_side_menu(context)

    assert len(menu) == 2
    assert menu[0]["app_label"] == "first_app"
    assert menu[1]["app_label"] == "second_app"


@pytest.mark.parametrize(
    "test_id,app_label,models,options,expected",
    [
        # Test ID 1: Basic model processing
        (
            "basic_processing",
            "test_app",
            [{"object_name": "TestModel", "admin_url": "/admin/test/model"}],
            {"icons": {}, "default_icon_children": "default-icon"},
            [
                {
                    "object_name": "TestModel",
                    "admin_url": "/admin/test/model",
                    "url": "/admin/test/model",
                    "model_str": "test_app.testmodel",
                    "icon": "default-icon",
                }
            ],
        ),
        # Test ID 2: Hidden model
        (
            "hidden_model",
            "test_app",
            [{"object_name": "TestModel", "admin_url": "/admin/test/model"}],
            {"hide_models": ["test_app.testmodel"], "icons": {}, "default_icon_children": "default-icon"},
            [],
        ),
        # Test ID 3: Custom icon
        (
            "custom_icon",
            "test_app",
            [{"object_name": "TestModel", "admin_url": "/admin/test/model"}],
            {"icons": {"test_app.testmodel": "custom-icon"}, "default_icon_children": "default-icon"},
            [
                {
                    "object_name": "TestModel",
                    "admin_url": "/admin/test/model",
                    "url": "/admin/test/model",
                    "model_str": "test_app.testmodel",
                    "icon": "custom-icon",
                }
            ],
        ),
        # Test ID 4: Multiple models
        (
            "multiple_models",
            "test_app",
            [
                {"object_name": "TestModel1", "admin_url": "/admin/test/model1"},
                {"object_name": "TestModel2", "admin_url": "/admin/test/model2"},
            ],
            {"icons": {}, "default_icon_children": "default-icon"},
            [
                {
                    "object_name": "TestModel1",
                    "admin_url": "/admin/test/model1",
                    "url": "/admin/test/model1",
                    "model_str": "test_app.testmodel1",
                    "icon": "default-icon",
                },
                {
                    "object_name": "TestModel2",
                    "admin_url": "/admin/test/model2",
                    "url": "/admin/test/model2",
                    "model_str": "test_app.testmodel2",
                    "icon": "default-icon",
                },
            ],
        ),
    ],
    ids=lambda x: x if isinstance(x, str) else "",
)
def test_process_models(test_id, app_label, models, options, expected):
    """
    Test the _process_models helper function with various scenarios:
    - Basic model processing
    - Hidden model filtering
    - Custom icon assignment
    - Multiple models processing
    """
    result = jazzmin._process_models(app_label, models, options)
    assert result == expected