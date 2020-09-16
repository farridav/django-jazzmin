import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models


class AllFields(models.Model):
    """
    This model represents all possible fields that Django supports
    """

    # Char
    char = models.CharField(
        default="Some Chars...",
        max_length=100,
        help_text="This is how CharFields look like..."
    )
    text = models.TextField(
        default="Some valuable Text...", help_text="This is how TextFields look like..."
    )
    slug = models.SlugField(
        default="slug", max_length=100, help_text="This is how SlugFields look like..."
    )
    email = models.EmailField(
        default="mrcheese@example.com",
        max_length=100,
        help_text="This is how EmailFields look like..."
    )

    # Number
    float = models.FloatField(
        default=10.0, help_text="This is how FloatFields look like..."
    )
    decimal = models.DecimalField(
        default=Decimal(10),
        decimal_places=4,
        max_digits=10,
        help_text="This is how DecimalFields look like..."
    )
    integer = models.IntegerField(
        default=10, help_text="This is how IntegerFields look like..."
    )
    small_integer = models.SmallIntegerField(
        default=1, help_text="This is how SmallIntegerFields look like..."
    )
    big_integer = models.BigIntegerField(
        default=1000000, help_text="This is how BigIntegerFields look like..."
    )
    positive_integer = models.PositiveIntegerField(
        default=1, help_text="This is how PositiveIntegerFields look like..."
    )

    # Boolean
    boolean = models.BooleanField(
        default=True, help_text="This is how BooleanFields look like..."
    )
    null_boolean = models.NullBooleanField(
        help_text="This is how NullBooleanFields look like..."
    )

    # Time
    date = models.DateField(
        help_text="This is how DateFields look like..."
    )
    date_time = models.DateTimeField(
        help_text="This is how DateTimeFields look like..."
    )
    time = models.TimeField(
        help_text="This is how TimeFields look like..."
    )

    # Files
    file_path = models.FilePathField(
        path=settings.BASE_DIR,
        help_text="This is how FilePathFields look like..."
    )
    file = models.FileField(
        upload_to='files',
        blank=True,
        null=True,
        help_text="This is how FileFields look like..."
    )

    # Other
    duration = models.DurationField(
        default=1, help_text="This is how DurationFields look like..."
    )
    identifier = models.UUIDField(
        default=uuid.uuid1(), help_text="This is how UUIDFields look like..."
    )
    generic_ip_address = models.GenericIPAddressField(
        default="127.0.0.1",
        help_text="This is how GenericIPAddressFields look like..."
    )

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = "AllFields"
