from random import choice

from django.contrib.auth.models import User, Group
from django.core.management import BaseCommand

from ...models import Book, Author, Genre
from ....factories import (
    BookLoanFactory,
    UserFactory,
    AuthorFactory,
    BookFactory,
    GroupFactory,
    LibraryFactory,
)
from ....loans.models import Library, BookLoan


class Command(BaseCommand):
    """
    A management script for resetting all data
    """

    def handle(self, *args, **options):
        for Model in [Group, User, Library, Author, Book, BookLoan, Genre]:
            Model.objects.all().delete()

        library = LibraryFactory()
        UserFactory(
            username="test@test.com",
            email="test@test.com",
            password="test",
            is_superuser=True,
        )

        users = UserFactory.create_batch(2, is_staff=False)

        GroupFactory.create_batch(5)

        for author in AuthorFactory.create_batch(10):
            for book in BookFactory.create_batch(5, author=author, library=library):
                BookLoanFactory(book=book, borrower=choice(users))

        self.stdout.write("All Data reset")
