from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone


class Library(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    librarian = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="library", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Libraries"

    def __str__(self):
        return self.address


class BookLoan(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        help_text="Unique ID for this particular book across whole library",
    )
    book = models.ForeignKey("books.Book", on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    loan_start = models.DateTimeField()
    due_back = models.DateField(null=True, blank=True)

    duration = models.DurationField(blank=True)

    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Book availability",
    )

    class Meta:
        ordering = ("due_back",)

    def __str__(self):
        return "{}, ({})".format(self.id, self.book.title)

    def save(self, **kwargs):
        self.duration = self.loan_start - timezone.now()
        super().save(**kwargs)
