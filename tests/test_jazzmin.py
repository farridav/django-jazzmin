from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class AdminlteTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create(
            email='test@test.com', password='test',
            is_staff=True, is_superuser=True, is_active=True
        )
        self.client.force_login(self.user)

    def test_menu_configuration(self):
        """
        All menu tweaking settings work as expected
        """
        pass

    def test_update_site_logo(self):
        """
        We can add a site logo, and it renders out
        """
        pass

    def test_ui_customisations(self):
        """
        All UI settings work as expected
        """
        pass
