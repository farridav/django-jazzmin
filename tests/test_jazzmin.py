import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_side_menu(admin_client):
    """
    All menu tweaking settings work as expected
    """
    url = reverse('admin:index')

    response = admin_client.get(url)
    app_list = response.context['app_list']

    # TODO: override settings, and confirm that our app_list is built the way we want it to
    # given that app_list is what builds out the menu and the dashboard
    assert app_list is not None


@pytest.mark.skip
def test_update_site_logo(admin_client):
    """
    We can add a site logo, and it renders out
    """
    pass


@pytest.mark.skip
def test_ui_customisations(admin_client):
    """
    All UI settings work as expected
    """
    pass


@pytest.mark.skip
def test_permissions_on_custom_links(admin_client):
    """
    We honour permissions for the rendering of custom links
    """
    pass


@pytest.mark.skip
def test_top_menu(admin_client):
    """
    Top menu renders out as expected
    """
    pass
