import uuid
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("admin:polls_poll_change", kwargs={"object_id": self.pk})

    def clean(self):
        if "cheese" not in self.text:
            raise ValidationError("Poll text must contain the word 'cheese'")

    def __str__(self):
        return self.text


class Choice(models.Model):
    """
    This model is just great
    """

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    def choice_text_with_cheese(self, cheese="Cheddar"):
        """
        It appends some cheese to your choice, as cheese is always a good choice
        """
        return "{} and {}".format(self.choice_text, cheese)

    def __str__(self):
        return self.choice_text[:25]


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Cheese(models.Model):
    name = models.CharField(max_length=40)
    stinky = models.BooleanField(
        default=False,
        help_text="Determines whether the cheese is stinky or not",
    )

    def __str__(self):
        return self.name


class Campaign(models.Model):
    polls = models.ManyToManyField(
        Poll,
        related_name="campaigns",
        help_text="The polls this campaign is part to",
    )
    cheese = models.ManyToManyField(
        Cheese,
        related_name="campaigns",
        help_text="The cheese that this campaign is fighting for",
    )
    promoter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The user promoting this campaign",
    )

    def __str__(self):
        return str(self.id)


class AllFields(models.Model):
    """
    This model contains all django core model fields
    """

    # Char
    char = models.CharField(
        default="Some Chars...",
        max_length=100,
        help_text="This is how CharFields look...",
    )
    text = models.TextField(
        default="Some valuable Text...",
        help_text="This is how TextFields look...",
    )
    slug = models.SlugField(
        default="slug",
        max_length=100,
        help_text="This is how SlugFields look...",
    )
    email = models.EmailField(
        default="mrcheese@example.com",
        max_length=100,
        help_text="This is how EmailFields look...",
    )

    # Number
    float = models.FloatField(
        default=10.0, help_text="This is how FloatFields look..."
    )
    decimal = models.DecimalField(
        default=Decimal(10),
        decimal_places=4,
        max_digits=10,
        help_text="This is how DecimalFields look...",
    )
    integer = models.IntegerField(
        default=10, help_text="This is how IntegerFields look..."
    )
    small_integer = models.SmallIntegerField(
        default=1, help_text="This is how SmallIntegerFields look..."
    )
    big_integer = models.BigIntegerField(
        default=1000000, help_text="This is how BigIntegerFields look..."
    )
    positive_integer = models.PositiveIntegerField(
        default=1, help_text="This is how PositiveIntegerFields look..."
    )

    # Boolean
    boolean = models.BooleanField(
        default=True, help_text="This is how BooleanFields look..."
    )
    null_boolean = models.NullBooleanField(
        help_text="This is how NullBooleanFields look..."
    )

    # Time
    date = models.DateField(help_text="This is how DateFields look...")
    date_time = models.DateTimeField(
        help_text="This is how DateTimeFields look..."
    )
    time = models.TimeField(help_text="This is how TimeFields look...")

    # Files
    file_path = models.FilePathField(
        path=settings.BASE_DIR, help_text="This is how FilePathFields look..."
    )
    file = models.FileField(
        upload_to="files",
        blank=True,
        null=True,
        help_text="This is how FileFields look...",
    )

    # Other
    duration = models.DurationField(
        default=1, help_text="This is how DurationFields look..."
    )
    identifier = models.UUIDField(
        default=uuid.uuid1(), help_text="This is how UUIDFields look..."
    )
    generic_ip_address = models.GenericIPAddressField(
        default="127.0.0.1",
        help_text="This is how GenericIPAddressFields look...",
    )

    # Relational
    many_to_many = models.ManyToManyField(
        Poll,
        related_name="+",
        help_text="This is how a many to many field looks...",
    )
    many_to_many_vertical = models.ManyToManyField(
        Poll,
        related_name="+",
        help_text="This is how a many to many field looks with filter_vertical...",
    )
    foreign_key = models.ForeignKey(
        Poll,
        related_name="+",
        on_delete=models.CASCADE,
        help_text="This is how a foreign key looks...",
        blank=True,
        null=True,
    )
    foreign_key_autocomplete = models.ForeignKey(
        Poll,
        related_name="+",
        on_delete=models.CASCADE,
        help_text="This is how a foreign key looks with autocomplete...",
        blank=True,
        null=True,
    )
    foreign_key_by_id = models.ForeignKey(
        Poll,
        related_name="+",
        on_delete=models.CASCADE,
        help_text="This is how a foreign key looks with raw_id_fields...",
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = "AllFields"
