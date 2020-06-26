import random

import pytest
from django.utils import timezone

from tests.test_app.polls.models import Poll, Vote, Choice


@pytest.fixture
def test_data(transactional_db, admin_user):
    dataset = {
        "How much cheese can you eat?": ["loads", "some", "all of it"],
        "Whats bigger than an elephant?": ["dog", "a bigger elephant", "mouldy cabbage"],
    }

    polls = []
    for question, answers in dataset.items():
        poll = Poll.objects.create(owner=admin_user, text=question, pub_date=timezone.now())

        choices = []
        for answer in answers:
            choices.append(Choice.objects.create(poll=poll, choice_text=answer))

        for x in range(1, random.randint(2, 10)):
            Vote.objects.create(user=admin_user, poll=poll, choice=random.choice(choices))

        polls.append(poll)

    return polls
