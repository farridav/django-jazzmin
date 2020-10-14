from django.contrib.auth.models import User, Group
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    """
    A management script for resetting all data
    """

    def handle(self, *args, **options):
        call_command("migrate")

        User.objects.all().delete()
        Group.objects.all().delete()

        call_command("loaddata", "initial_data")

        self.stdout.write("All Data reset")
