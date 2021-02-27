from datetime import date, timedelta

import factory
from django.contrib.auth.models import Group, Permission, User
from django.utils import timezone
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyInteger

from .books.models import Author, Book, Genre
from .loans.models import BookLoan, Library

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

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        """
        Create a user with the given permissions, e.g UserFactory(permissions=('books.view_book', 'auth.change_user'))
        """
        if not create:
            return

        if extracted:
            available_permissions = [
                "{}.{}".format(x[0], x[1])
                for x in Permission.objects.values_list("content_type__app_label", "codename")
            ]

            for permission in extracted:
                assert permission in available_permissions, "{} not in {}".format(permission, available_permissions)

                app, perm = permission.split(".")
                perm_obj = Permission.objects.get(content_type__app_label=app, codename=perm)

                self.user_permissions.add(perm_obj)

    class Meta:
        model = User


class GenreFactory(DjangoModelFactory):
    name = factory.Faker("job")

    class Meta:
        model = Genre


class AuthorFactory(DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    date_of_birth = FuzzyDate(date(1950, 1, 1), NOW.date() - timedelta(days=365))
    date_of_death = factory.LazyAttribute(
        lambda x: x.date_of_birth.replace(year=NOW.year, day=min(28, x.date_of_birth.day))
    )

    class Meta:
        model = Author


class LibraryFactory(DjangoModelFactory):
    name = factory.Faker("company")
    address = factory.Faker("address")
    librarian = factory.SubFactory(UserFactory)

    class Meta:
        model = Library


class BookFactory(DjangoModelFactory):
    title = factory.Faker("sentence")
    author = factory.SubFactory(AuthorFactory)
    library = factory.SubFactory(LibraryFactory)
    summary = factory.Faker("sentence")
    isbn = "9780123456472"
    published_on = FuzzyDate(date(1950, 1, 1), date(1999, 1, 1))
    last_print = FuzzyDate(date(2000, 1, 1), date(2020, 1, 1))
    pages = FuzzyInteger(50, 1000)

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
    status = FuzzyChoice(dict(BookLoan.LOAN_STATUS).keys())

    class Meta:
        model = BookLoan
