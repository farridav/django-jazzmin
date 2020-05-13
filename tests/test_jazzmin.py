import pytest


@pytest.mark.django_db
def test_menu_configuration(admin_client):
    """
    All menu tweaking settings work as expected
    """
    pass


@pytest.mark.django_db
def test_update_site_logo(admin_client):
    """
    We can add a site logo, and it renders out
    """
    pass


@pytest.mark.django_db
def test_ui_customisations(admin_client):
    """
    All UI settings work as expected
    """
    pass
