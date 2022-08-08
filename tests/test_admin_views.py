import re
import django
import pytest
from jazzmin.compat import reverse

from .test_app.library.books.models import Book
from .test_app.library.factories import BookFactory


@pytest.mark.django_db
def test_login(client, admin_user):
    """
    We can render the login page
    """
    url = reverse("admin:login")

    response = client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    assert templates_used == [
        "admin/login.html",
        "registration/base.html",
    ]

    response = client.post(
        url + "?next=/admin/",
        data={"username": admin_user.username, "password": "password"},
        follow=True,
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
    assert templates_used == [
        "registration/logged_out.html",
        "registration/base.html",
    ]


@pytest.mark.django_db
def test_reset_password(client, admin_user):
    """
    We can render the password reset views
    """
    # Step 1: Password reset form
    url = reverse("admin_password_reset")

    response = client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    assert templates_used == [
        "registration/password_reset_form.html",
        "registration/base.html",
    ]

    # Step 2: Password reset done
    response = client.post(
        url,
        data={"email": admin_user.email},
        follow=True,
    )
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    assert response.resolver_match.url_name == "password_reset_done"
    assert templates_used == [
        "registration/password_reset_done.html",
        "registration/base.html",
    ]
    assert "We’ve emailed you instructions for setting your password" in response.content.decode()

    # Get password reset link from reset email
    email = django.core.mail.outbox[0]
    url = re.search(r"https?://[^/]*(/.*reset/\S*)", email.body).group(1)

    # Step 3: Password reset confirm
    response = client.get(url, follow=True)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    assert response.resolver_match.url_name == "password_reset_confirm"
    assert templates_used == [
        "registration/password_reset_confirm.html",
        "registration/base.html",
    ]

    # Step 4: Password reset complete
    response = client.post(
        response.request["PATH_INFO"],
        data={"username": admin_user.username, "new_password1": "new_password", "new_password2": "new_password"},
        follow=True,
    )
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    assert response.resolver_match.url_name == "password_reset_complete"
    assert templates_used == [
        "registration/password_reset_complete.html",
        "registration/base.html",
    ]
    assert "Your password has been set." in response.content.decode()


@pytest.mark.django_db
def test_password_change(admin_client):
    """
    We can render the password change form, and successfully change our password
    """
    url = reverse("admin:password_change")

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]
    expected_templates_used = {
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

    if django.VERSION[0] == 4:
        expected_templates_used.update({"django/forms/errors/list/default.html", "django/forms/errors/list/ul.html"})

    assert response.status_code == 200
    assert set(templates_used) == expected_templates_used

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

    expected_render_counts = {
        "admin/base.html": 1,
        "admin/base_site.html": 1,
        "admin/change_form.html": 1,
        "admin/change_form_object_tools.html": 1,
        "admin/edit_inline/stacked.html": 1,
        "admin/includes/fieldset.html": 4,
        "admin/prepopulated_fields_js.html": 1,
        "admin/submit_line.html": 1,
        "admin/widgets/foreign_key_raw_id.html": 1,
        "admin/widgets/related_widget_wrapper.html": 4,
        "admin/widgets/split_datetime.html": 2,
        "django/forms/widgets/attrs.html": 47,
        "django/forms/widgets/date.html": 5,
        "django/forms/widgets/hidden.html": 6,
        "django/forms/widgets/input.html": 19,
        "django/forms/widgets/number.html": 1,
        "django/forms/widgets/select.html": 6,
        "django/forms/widgets/select_option.html": 21,
        "django/forms/widgets/text.html": 4,
        "django/forms/widgets/textarea.html": 1,
        "django/forms/widgets/time.html": 2,
        "jazzmin/includes/horizontal_tabs.html": 1,
        "jazzmin/includes/ui_builder_panel.html": 1,
    }

    if django.VERSION[0] == 4:
        expected_render_counts.update(
            {
                "django/forms/div.html": 1,
                "django/forms/errors/list/default.html": 2,
                "django/forms/errors/list/ul.html": 56,
            }
        )

    # The number of times each template was rendered
    assert render_counts == expected_render_counts

    expected_templates_used = {
        "admin/base.html",
        "admin/base_site.html",
        "admin/change_form.html",
        "admin/change_form_object_tools.html",
        "admin/edit_inline/stacked.html",
        "admin/includes/fieldset.html",
        "admin/prepopulated_fields_js.html",
        "admin/submit_line.html",
        "admin/widgets/foreign_key_raw_id.html",
        "admin/widgets/related_widget_wrapper.html",
        "admin/widgets/split_datetime.html",
        "django/forms/widgets/attrs.html",
        "django/forms/widgets/date.html",
        "django/forms/widgets/hidden.html",
        "django/forms/widgets/input.html",
        "django/forms/widgets/number.html",
        "django/forms/widgets/select.html",
        "django/forms/widgets/select_option.html",
        "django/forms/widgets/text.html",
        "django/forms/widgets/textarea.html",
        "django/forms/widgets/time.html",
        "jazzmin/includes/horizontal_tabs.html",
        "jazzmin/includes/ui_builder_panel.html",
    }

    if django.VERSION[0] == 4:
        expected_templates_used.update(
            {
                "django/forms/div.html",
                "django/forms/errors/list/default.html",
                "django/forms/errors/list/ul.html",
            }
        )

    # The templates that were used
    assert set(templates_used) == expected_templates_used

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

    expected_render_counts = {
        "admin/actions.html": 2,
        "admin/base.html": 1,
        "admin/base_site.html": 1,
        "admin/change_list.html": 1,
        "admin/change_list_object_tools.html": 1,
        "admin/change_list_results.html": 1,
        "admin/date_hierarchy.html": 1,
        "admin/pagination.html": 1,
        "admin/search_form.html": 1,
        "django/forms/widgets/attrs.html": 27,
        "django/forms/widgets/checkbox.html": 5,
        "django/forms/widgets/hidden.html": 11,
        "django/forms/widgets/input.html": 21,
        "django/forms/widgets/select.html": 2,
        "django/forms/widgets/select_option.html": 4,
        "django/forms/widgets/text.html": 5,
        "jazzmin/includes/ui_builder_panel.html": 1,
    }

    if django.VERSION[0] == 4:
        expected_render_counts.update(
            {
                "django/forms/div.html": 1,
                "django/forms/errors/list/default.html": 6,
                "django/forms/errors/list/ul.html": 6,
            }
        )

    # The number of times each template was rendered
    assert render_counts == expected_render_counts

    expected_templates = {
        "admin/actions.html",
        "admin/base.html",
        "admin/base_site.html",
        "admin/change_list.html",
        "admin/change_list_object_tools.html",
        "admin/change_list_results.html",
        "admin/date_hierarchy.html",
        "admin/pagination.html",
        "admin/search_form.html",
        "django/forms/widgets/attrs.html",
        "django/forms/widgets/checkbox.html",
        "django/forms/widgets/hidden.html",
        "django/forms/widgets/input.html",
        "django/forms/widgets/select.html",
        "django/forms/widgets/select_option.html",
        "django/forms/widgets/text.html",
        "jazzmin/includes/ui_builder_panel.html",
    }

    if django.VERSION[0] == 4:
        expected_templates.update(
            {
                "django/forms/div.html",
                "django/forms/errors/list/default.html",
                "django/forms/errors/list/ul.html",
            }
        )

    # The templates that were used
    assert set(templates_used) == expected_templates


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
