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
        self.client.force_login(self.user)

    def test_smoke(self):
        """
        We can render the admin out with nothing broken
        """
        url = reverse('admin:index')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_options_admin(self):
        url = reverse('admin:index')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_menu_admin(self):
        url = reverse('admin:general_option')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_update_options(self):
        """

        /admin/django_admin_settings/options/   django.contrib.admin.options.changelist_view    admin:django_admin_settings_options_changelist
        /admin/django_admin_settings/options/<path:object_id>/  django.views.generic.base.RedirectView
        /admin/django_admin_settings/options/<path:object_id>/change/   django.contrib.admin.options.change_view        admin:django_admin_settings_options_change
        /admin/django_admin_settings/options/<path:object_id>/delete/   django.contrib.admin.options.delete_view        admin:django_admin_settings_options_delete
        /admin/django_admin_settings/options/<path:object_id>/history/  django.contrib.admin.options.history_view       admin:django_admin_settings_options_history
        /admin/django_admin_settings/options/add/       django.contrib.admin.options.add_view   admin:django_admin_settings_options_add
        /admin/django_admin_settings/options/autocomplete/      django.contrib.admin.options.autocomplete_view  admin:django_admin_settings_options_autocomplete
        /admin/django_admin_settings/options/general_option/    adminlteui.admin.general_option_view    admin:general_option

        """
        url = reverse('admin:general_option')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_update_site_logo(self):
        url = reverse('admin:general_option')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_exchange_menu(self):
        url = reverse('admin:general_option')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_build_custom_menu(self):
        url = reverse('admin:exchange_menu')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_templates_used(self):
        pass
