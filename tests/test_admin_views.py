import pytest

from jazzmin.compat import reverse
from tests.factories import BookFactory
from tests.test_app.books.models import Book


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
def test_detail(admin_client):
    """
    We can render the detail view
    """
    book = BookFactory()
    url = reverse("admin:books_book_change", args=(book.pk,))

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    render_counts = {x: templates_used.count(x) for x in set(templates_used)}

    # The number of times each template was rendered
    assert render_counts == {
        "django/forms/widgets/text.html": 6,
        "admin/widgets/foreign_key_raw_id.html": 1,
        "django/forms/widgets/select_option.html": 19,
        "admin/edit_inline/stacked.html": 1,
        "admin/prepopulated_fields_js.html": 1,
        "jazzmin/includes/ui_builder_panel.html": 1,
        "admin/widgets/related_widget_wrapper.html": 3,
        "django/forms/widgets/textarea.html": 1,
        "admin/change_form_object_tools.html": 1,
        "django/forms/widgets/date.html": 3,
        "admin/base.html": 1,
        "admin/includes/fieldset.html": 4,
        "django/forms/widgets/hidden.html": 6,
        "django/forms/widgets/attrs.html": 41,
        "admin/change_form.html": 1,
        "admin/base_site.html": 1,
        "django/forms/widgets/select.html": 5,
        "jazzmin/includes/horizontal_tabs.html": 1,
        "django/forms/widgets/input.html": 16,
        "admin/submit_line.html": 1,
    }

    # The templates that were used
    assert set(templates_used) == {
        "django/forms/widgets/text.html",
        "admin/widgets/foreign_key_raw_id.html",
        "django/forms/widgets/select_option.html",
        "admin/edit_inline/stacked.html",
        "admin/prepopulated_fields_js.html",
        "jazzmin/includes/ui_builder_panel.html",
        "admin/widgets/related_widget_wrapper.html",
        "django/forms/widgets/textarea.html",
        "admin/change_form_object_tools.html",
        "django/forms/widgets/date.html",
        "admin/base.html",
        "admin/includes/fieldset.html",
        "django/forms/widgets/hidden.html",
        "django/forms/widgets/attrs.html",
        "admin/change_form.html",
        "admin/base_site.html",
        "django/forms/widgets/select.html",
        "jazzmin/includes/horizontal_tabs.html",
        "django/forms/widgets/input.html",
        "admin/submit_line.html",
    }

    # TODO: post data and confirm we can change model instances


@pytest.mark.django_db
def test_list(admin_client):
    """
    We can render the list view
    """
    BookFactory.create_batch(5)

    url = reverse("admin:books_book_changelist")

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    render_counts = {x: templates_used.count(x) for x in set(templates_used)}

    # The number of times each template was rendered
    assert render_counts == {
        "jazzmin/includes/ui_builder_panel.html": 1,
        "admin/change_list.html": 1,
        "django/forms/widgets/checkbox.html": 5,
        "django/forms/widgets/text.html": 5,
        "django/forms/widgets/select_option.html": 4,
        "admin/filter.html": 2,
        "admin/base.html": 1,
        "admin/base_site.html": 1,
        "admin/change_list_object_tools.html": 1,
        "admin/date_hierarchy.html": 1,
        "django/forms/widgets/select.html": 2,
        "admin/change_list_results.html": 1,
        "admin/pagination.html": 1,
        "django/forms/widgets/input.html": 21,
        "admin/search_form.html": 1,
        "django/forms/widgets/hidden.html": 11,
        "django/forms/widgets/attrs.html": 27,
        "admin/actions.html": 2,
    }

    # The templates that were used
    assert set(templates_used) == {
        "jazzmin/includes/ui_builder_panel.html",
        "admin/change_list.html",
        "django/forms/widgets/checkbox.html",
        "django/forms/widgets/text.html",
        "django/forms/widgets/select_option.html",
        "admin/filter.html",
        "admin/base.html",
        "admin/base_site.html",
        "admin/change_list_object_tools.html",
        "admin/date_hierarchy.html",
        "django/forms/widgets/select.html",
        "admin/change_list_results.html",
        "admin/pagination.html",
        "django/forms/widgets/input.html",
        "admin/search_form.html",
        "django/forms/widgets/hidden.html",
        "django/forms/widgets/attrs.html",
        "admin/actions.html",
    }


@pytest.mark.django_db
def test_history(admin_client):
    """
    We can render the object history page
    """
    book = BookFactory()
    url = reverse("admin:books_book_history", args=(book.pk,))

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
def test_delete(admin_client):
    """
    We can load the confirm delete page, and POST it, and it deletes our object
    """
    book = BookFactory()
    url = reverse("admin:books_book_delete", args=(book.pk,))

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
    assert not Book.objects.all().exists()
    assert response.resolver_match.url_name == "books_book_changelist"
