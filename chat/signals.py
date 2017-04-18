from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import *


@receiver(user_logged_in)
def on_user_login(sender, **kwargs):
    Person.objects.filter(user=kwargs.get('user')).update(online=1)


@receiver(user_logged_out)
def on_user_logout(sender, **kwargs):
    Person.objects.filter(user=kwargs.get('user')).update(online=0)