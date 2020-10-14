from datetime import timedelta, date

import factory
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils import timezone
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDate

from tests.test_app.books.models import Author, Book, Genre
from tests.test_app.loans.models import BookLoan, Library

NOW = timezone.now()


class GroupFactory(DjangoModelFactory):
    name = factory.Faker("job")

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.permissions.add(group)

    class Meta:
        model = Group


class UserFactory(DjangoModelFactory):
    username = factory.Faker("name")
    email = factory.Faker("email")
    is_staff = True
    is_active = True
    is_superuser = False
    password = factory.PostGenerationMethodCall("set_password", "test")

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)

    class Meta:
        model = settings.AUTH_USER_MODEL


class GenreFactory(DjangoModelFactory):
    name = factory.Faker("job")

    class Meta:
        model = Genre


class AuthorFactory(DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    date_of_birth = FuzzyDate(date(1950, 1, 1), NOW.date() - timedelta(days=365))
    date_of_death = factory.LazyAttribute(lambda x: x.date_of_birth.replace(year=NOW.year))

    class Meta:
        model = Author


class LibraryFactory(DjangoModelFactory):
    address = factory.Faker("address")
    librarian = factory.SubFactory(UserFactory)

    class Meta:
        model = Library


class BookFactory(DjangoModelFactory):
    title = factory.Faker("sentence")
    author = factory.SubFactory(AuthorFactory)
    library = factory.SubFactory(LibraryFactory)
    summary = factory.Faker("sentence")
    isbn = factory.Faker("isbn13")
    published_on = FuzzyDate(date(1950, 1, 1), date(1999, 1, 1))

    @factory.post_generation
    def genre(self, create, extracted, **kwargs):
        if not create:
            return

        extracted = extracted or GenreFactory.create_batch(3)
        for genre in extracted:
            self.genre.add(genre)

    class Meta:
        model = Book


class BookLoanFactory(DjangoModelFactory):
    id = factory.Faker("uuid4")
    book = factory.SubFactory(BookFactory)
    imprint = factory.Faker("name")
    loan_start = NOW
    due_back = factory.LazyAttribute(lambda x: x.loan_start + timedelta(weeks=2))
    borrower = factory.SubFactory(UserFactory)
    status = factory.fuzzy.FuzzyChoice(dict(BookLoan.LOAN_STATUS).keys())

    class Meta:
        model = BookLoan
