from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AdminlteTestCase(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create(
            email='test@test.com', password='test',
            is_staff=True, is_superuser=True, is_active=True
        )

    def test_smoke(self):
        self.client.force_login(self.user)

        url = reverse('admin:index')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_options_admin(self):
        pass

    def test_menu_admin(self):
        pass

    def test_update_options(self):
        pass

    def test_update_site_logo(self):
        pass

    def test_exchange_menu(self):
        pass

    def test_build_custom_menu(self):
        pass
