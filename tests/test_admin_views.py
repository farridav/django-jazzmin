import pytest

from jazzmin.compat import reverse
from tests.test_app.polls.models import Poll


@pytest.mark.django_db
def test_login(client, admin_user):
    """
    We can render the login page
    """
    url = reverse("admin:login")

    response = client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    assert templates_used == ["admin/login.html"]

    response = client.post(
        url + "?next=/admin/", data={"username": admin_user.username, "password": "password"}, follow=True
    )

    assert response.status_code == 200
    assert "dashboard" in response.content.decode()


@pytest.mark.django_db
def test_logout(admin_client):
    """
    We can log out, and render the logout page
    """
    url = reverse("admin:logout")

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    assert templates_used == ["registration/logged_out.html"]


@pytest.mark.django_db
def test_password_change(admin_client):
    """
    We can render the password change form, and successfully change our password
    """
    url = reverse("admin:password_change")

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    assert set(templates_used) == {
        "registration/password_change_form.html",
        "admin/base_site.html",
        "admin/base.html",
        "django/forms/widgets/password.html",
        "django/forms/widgets/input.html",
        "django/forms/widgets/attrs.html",
        "django/forms/widgets/password.html",
        "django/forms/widgets/input.html",
        "django/forms/widgets/attrs.html",
        "django/forms/widgets/password.html",
        "django/forms/widgets/input.html",
        "django/forms/widgets/attrs.html",
        "jazzmin/includes/ui_builder_panel.html",
    }

    response = admin_client.post(
        url,
        data={"old_password": "password", "new_password1": "PickleRick123!!", "new_password2": "PickleRick123!!"},
        follow=True,
    )
    templates_used = [t.name for t in response.templates]

    assert "Password change successful" in response.content.decode()
    assert set(templates_used) == {
        "registration/password_change_done.html",
        "admin/base.html",
        "admin/base_site.html",
        "jazzmin/includes/ui_builder_panel.html",
    }


@pytest.mark.django_db
def test_dashboard(admin_client):
    """
    We can render the dashboard
    """
    url = reverse("admin:index")

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    assert templates_used == [
        "admin/index.html",
        "admin/base_site.html",
        "admin/base.html",
        "jazzmin/includes/ui_builder_panel.html",
    ]


@pytest.mark.django_db
def test_detail(admin_client, test_data):
    """
    We can render the detail view
    """
    url = reverse("admin:polls_poll_change", args=(test_data[0].pk,))

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    render_counts = {x: templates_used.count(x) for x in set(templates_used)}

    # The number of times each template was rendered
    assert render_counts == {
        "admin/base.html": 1,
        "admin/base_site.html": 1,
        "admin/change_form.html": 1,
        "admin/change_form_object_tools.html": 1,
        "admin/edit_inline/stacked.html": 1,
        "admin/includes/fieldset.html": 7,
        "admin/prepopulated_fields_js.html": 1,
        "admin/submit_line.html": 1,
        "admin/widgets/foreign_key_raw_id.html": 1,
        "admin/widgets/split_datetime.html": 1,
        "django/forms/widgets/attrs.html": 29,
        "django/forms/widgets/checkbox.html": 4,
        "django/forms/widgets/date.html": 2,
        "django/forms/widgets/hidden.html": 14,
        "django/forms/widgets/input.html": 28,
        "django/forms/widgets/multiwidget.html": 1,
        "django/forms/widgets/splithiddendatetime.html": 1,
        "django/forms/widgets/text.html": 5,
        "django/forms/widgets/textarea.html": 1,
        "django/forms/widgets/time.html": 2,
        "jazzmin/includes/horizontal_tabs.html": 1,
        "jazzmin/includes/ui_builder_panel.html": 1,
    }

    # The templates that were used
    assert set(templates_used) == {
        "admin/base.html",
        "admin/base_site.html",
        "admin/change_form.html",
        "admin/change_form_object_tools.html",
        "admin/edit_inline/stacked.html",
        "admin/includes/fieldset.html",
        "admin/prepopulated_fields_js.html",
        "admin/submit_line.html",
        "admin/widgets/foreign_key_raw_id.html",
        "admin/widgets/split_datetime.html",
        "django/forms/widgets/attrs.html",
        "django/forms/widgets/checkbox.html",
        "django/forms/widgets/date.html",
        "django/forms/widgets/hidden.html",
        "django/forms/widgets/input.html",
        "django/forms/widgets/multiwidget.html",
        "django/forms/widgets/splithiddendatetime.html",
        "django/forms/widgets/text.html",
        "django/forms/widgets/textarea.html",
        "django/forms/widgets/time.html",
        "jazzmin/includes/horizontal_tabs.html",
        "jazzmin/includes/ui_builder_panel.html",
    }

    # TODO: post data and confirm we can change model instances


@pytest.mark.django_db
def test_list(admin_client, test_data):
    """
    We can render the list view
    """
    url = reverse("admin:polls_poll_changelist")

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    render_counts = {x: templates_used.count(x) for x in set(templates_used)}

    # The number of times each template was rendered
    assert render_counts == {
        "admin/actions.html": 2,
        "admin/base.html": 1,
        "admin/base_site.html": 1,
        "admin/change_list.html": 1,
        "admin/change_list_object_tools.html": 1,
        "admin/change_list_results.html": 1,
        "admin/date_hierarchy.html": 1,
        "admin/filter.html": 1,
        "admin/pagination.html": 1,
        "admin/search_form.html": 1,
        "django/forms/widgets/attrs.html": 18,
        "django/forms/widgets/checkbox.html": 4,
        "django/forms/widgets/hidden.html": 8,
        "django/forms/widgets/input.html": 12,
        "django/forms/widgets/select.html": 2,
        "django/forms/widgets/select_option.html": 4,
        "jazzmin/includes/ui_builder_panel.html": 1,
    }

    # The templates that were used
    assert set(templates_used) == {
        "admin/actions.html",
        "admin/base.html",
        "admin/base_site.html",
        "admin/change_list.html",
        "admin/change_list_object_tools.html",
        "admin/change_list_results.html",
        "admin/date_hierarchy.html",
        "admin/filter.html",
        "admin/pagination.html",
        "admin/search_form.html",
        "django/forms/widgets/attrs.html",
        "django/forms/widgets/checkbox.html",
        "django/forms/widgets/hidden.html",
        "django/forms/widgets/input.html",
        "django/forms/widgets/select.html",
        "django/forms/widgets/select_option.html",
        "jazzmin/includes/ui_builder_panel.html",
    }


@pytest.mark.django_db
def test_history(admin_client, test_data):
    """
    We can render the object history page
    """
    poll = test_data[0]
    url = reverse("admin:polls_poll_history", args=(poll.pk,))

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    render_counts = {x: templates_used.count(x) for x in set(templates_used)}

    # The number of times each template was rendered
    assert render_counts == {
        "admin/object_history.html": 1,
        "admin/base.html": 1,
        "admin/base_site.html": 1,
        "jazzmin/includes/ui_builder_panel.html": 1,
    }

    # The templates that were used
    assert set(templates_used) == {
        "admin/object_history.html",
        "admin/base.html",
        "admin/base_site.html",
        "jazzmin/includes/ui_builder_panel.html",
    }


@pytest.mark.django_db
def test_delete(admin_client, test_data):
    """
    We can load the confirm delete page, and POST it, and it deletes our object
    """
    poll = test_data[0]
    url = reverse("admin:polls_poll_delete", args=(poll.pk,))

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    render_counts = {x: templates_used.count(x) for x in set(templates_used)}

    # The number of times each template was rendered
    assert render_counts == {
        "admin/delete_confirmation.html": 1,
        "admin/base_site.html": 1,
        "admin/base.html": 1,
        "admin/includes/object_delete_summary.html": 1,
        "jazzmin/includes/ui_builder_panel.html": 1,
    }

    # The templates that were used
    assert set(templates_used) == {
        "admin/delete_confirmation.html",
        "admin/base_site.html",
        "admin/base.html",
        "admin/includes/object_delete_summary.html",
        "jazzmin/includes/ui_builder_panel.html",
    }

    response = admin_client.post(url, data={"post": "yes"}, follow=True)

    # We deleted our object, and are now back on the changelist
    assert not Poll.objects.filter(id=poll.pk).exists()
    assert response.resolver_match.url_name == "polls_poll_changelist"
