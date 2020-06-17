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
        return reverse('admin:polls_poll_change', kwargs={'object_id': self.pk})

    def clean(self):
        if 'cheese' in self.text:
            raise ValidationError('cheese cannot be in the poll text')

    def __str__(self):
        return self.text


class Choice(models.Model):
    """
    This model is just great
    """
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    def choice_text_with_cheese(self, cheese='Cheddar'):
        """
        It appends some cheese to your choice, as cheese is always a good choice
        """
        return '{} and {}'.format(self.choice_text, cheese)

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
        help_text='Determines whether the cheese is stinky or not'
    )

    def __str__(self):
        return self.name


class Campaign(models.Model):
    polls = models.ManyToManyField(
        Poll,
        related_name='campaigns',
        help_text='The polls this campaign is part to'
    )
    cheese = models.ManyToManyField(
        Cheese,
        related_name='campaigns',
        help_text='The cheese that this campaign is fighting for'
    )
    promoter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text='The user promoting this campaign'
    )

    def __str__(self):
        return str(self.id)
