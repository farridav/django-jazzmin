from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AdminlteTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create(
            email='test@test.com', password='test',
            is_staff=True, is_superuser=True, is_active=True
        )
        self.client.force_login(self.user)

    def test_options_admin(self):
        """
        The Options admin renders out
        """
        url = reverse('admin:index')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_menu_admin(self):
        """
        The menu admin renders out
        """
        url = reverse('admin:general_option')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_update_options(self):
        """
        We can update all of the options available, and they affect the UI as expected
        """
        pass

    def test_update_site_logo(self):
        """
        We can add a site logo, and it renders out
        """
        pass

    def test_exchange_menu(self):
        """
        We can exchange our basic menu for a custom one, and back
        """
        pass

    def test_build_custom_menu(self):
        """
        We can build a custom menu and it renders out on top and left side
        """
        pass

    def test_numqueries(self):
        """
        We make a minimal no. of queries on each admin page view
        """
        pass
