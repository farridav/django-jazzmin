import pytest

from jazzmin.compat import reverse


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
    }

    response = admin_client.post(
        url,
        data={"old_password": "password", "new_password1": "PickleRick123!!", "new_password2": "PickleRick123!!"},
        follow=True,
    )
    templates_used = [t.name for t in response.templates]

    assert "Password change successful" in response.content.decode()
    assert set(templates_used) == {"registration/password_change_done.html", "admin/base.html", "admin/base_site.html"}


@pytest.mark.django_db
def test_dashboard(admin_client):
    """
    We can render the dashboard
    """
    url = reverse("admin:index")

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    assert templates_used == ["admin/index.html", "admin/base_site.html", "admin/base.html"]
