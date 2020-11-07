from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def add_user_levels_actions(sender, instance, **kwargs):
    """
    Dont allow our test user to change their password
    """
    if instance.username == "test@test.com":
        instance.set_password("test")
