from random import choice

from django.contrib.auth.models import Group, User
from django.core.management import BaseCommand

from ....factories import (
    AuthorFactory,
    BookFactory,
    BookLoanFactory,
    GroupFactory,
    LibraryFactory,
    UserFactory,
)
from ....loans.models import BookLoan, Library
from ...models import Author, Book, Genre


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
