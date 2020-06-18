import os

from django.apps import AppConfig


class PollsConfig(AppConfig):
    name = 'polls' if os.getenv('STANDALONE') else 'tests.test_app.polls'
