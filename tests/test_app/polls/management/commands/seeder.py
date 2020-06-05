import datetime
import random
import time
from logging import getLogger

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from faker import Faker

from ...models import Choice, Poll, Vote

fake = Faker()
logger = getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.seed_all()

    def seed_users(self, num_entries=10, overwrite=False):
        """
        Creates num_entries worth a new users
        """
        if overwrite:
            print("Overwriting Users")
            User.objects.all().delete()
        count = 0
        for _ in range(num_entries):
            first_name = fake.first_name()
            last_name = fake.last_name()
            User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=first_name + "." + last_name + "@fakermail.com",
                username=first_name + last_name,
                password="password",
            )
            count += 1
            percent_complete = count / num_entries * 100
            print("Adding {} new Users: {:.2f}%".format(num_entries, percent_complete), end="\r", flush=True)
        print()

    def seed_polls(self, num_entries=10, choice_min=2, choice_max=5, overwrite=False):
        """
        Seeds num_entries poll with random users as owners
        Each poll will be seeded with # choices from choice_min to choice_max
        """
        if overwrite:
            print("Overwriting polls")
            Poll.objects.all().delete()
        users = list(User.objects.all())
        count = 0
        for _ in range(num_entries):
            p = Poll(owner=random.choice(users), text=fake.paragraph(), pub_date=datetime.datetime.now(), )
            p.save()
            num_choices = random.randrange(choice_min, choice_max + 1)
            for _ in range(num_choices):
                Choice(poll=p, choice_text=fake.sentence()).save()
            count += 1
            percent_complete = count / num_entries * 100
            print("Adding {} new Polls: {:.2f}%".format(num_entries, percent_complete), end="\r", flush=True)
        print()

    def seed_votes(self):
        """
        Creates a new vote on every poll for every user
        Voted for choice is selected random.
        Deletes all votes prior to adding new ones
        """
        Vote.objects.all().delete()
        users = User.objects.all()
        polls = Poll.objects.all()
        count = 0
        number_of_new_votes = users.count() * polls.count()
        for poll in polls:
            choices = list(poll.choice_set.all())
            for user in users:
                Vote(user=user, poll=poll, choice=random.choice(choices)).save()
                count += 1
                percent_complete = count / number_of_new_votes * 100
                print(
                    "Adding {} new votes: {:.2f}%".format(number_of_new_votes, percent_complete), end="\r", flush=True,
                )
        print()

    def seed_all(self, num_entries=10, overwrite=False):
        """
        Runs all seeder functions. Passes value of overwrite to all
        seeder function calls.
        """
        start_time = time.time()
        # run seeds
        self.seed_users(num_entries=num_entries, overwrite=overwrite)
        self.seed_polls(num_entries=num_entries, overwrite=overwrite)
        self.seed_votes()
        # get time
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        print("Script Execution took: {} minutes {} seconds".format(minutes, seconds))
