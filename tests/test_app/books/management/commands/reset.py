from random import choice

from django.core.management import BaseCommand, call_command

from tests.factories import BookLoanFactory, UserFactory, AuthorFactory, BookFactory, GroupFactory, LibraryFactory


class Command(BaseCommand):
    """
    A management script for resetting all data
    """

    def handle(self, *args, **options):
        call_command("reset_db", "--noinput")
        call_command("migrate")

        library = LibraryFactory()
        UserFactory(username="test@test.com", email="test@test.com", password="test", is_superuser=True)

        users = UserFactory.create_batch(2, is_staff=False)

        GroupFactory.create_batch(5)

        for author in AuthorFactory.create_batch(10):
            for book in BookFactory.create_batch(5, author=author, library=library):
                BookLoanFactory(book=book, borrower=choice(users))

        self.stdout.write("All Data reset")
