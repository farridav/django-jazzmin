import pytest

from jazzmin.compat import reverse


@pytest.mark.django_db
def test_login(client, admin_user):
    url = reverse('admin:login')
    client.force_login(admin_user)

    response = client.get(url, follow=True)

    assert response.status_code == 200


@pytest.mark.django_db
def test_dashboard(client, admin_user):
    url = reverse('admin:index')
    client.force_login(admin_user)

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_list_view(client, admin_user):
    pass


@pytest.mark.django_db
def test_detail_view(client, admin_user):
    pass


@pytest.mark.django_db
def test_history_view(client, admin_user):
    pass
