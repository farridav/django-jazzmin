import pytest

from jazzmin.compat import reverse


@pytest.mark.django_db
def test_login(admin_client):
    url = reverse('admin:login')

    response = admin_client.get(url, follow=True)

    assert response.status_code == 200


@pytest.mark.django_db
def test_dashboard(admin_client):
    url = reverse('admin:index')

    response = admin_client.get(url)

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
