import pytest


@pytest.mark.django_db
def test_menu_configuration(client, admin_user):
    """
    All menu tweaking settings work as expected
    """
    pass


@pytest.mark.django_db
def test_update_site_logo(client, admin_user):
    """
    We can add a site logo, and it renders out
    """
    pass


@pytest.mark.django_db
def test_ui_customisations(client, admin_user):
    """
    All UI settings work as expected
    """
    pass
