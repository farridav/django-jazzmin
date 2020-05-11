from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class SmokeTestCase(TestCase):
    """
    Smoke test rendering of various admin views with jazzmin app installed
    """

    def setUp(self):
        super().setUp()
        self.user = User.objects.create(
            email='test@test.com', password='test',
            is_staff=True, is_superuser=True, is_active=True
        )

    def test_login(self):
        url = reverse('admin:login')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_dashboard(self):
        url = reverse('admin:index')
        self.client.force_login(self.user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_list_view(self):
        pass

    def test_detail_view(self):
        pass

    def test_history_view(self):
        pass
