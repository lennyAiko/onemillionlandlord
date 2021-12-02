from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Staff
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from django.dispatch import receiver


def staff_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='staff')
        instance.groups.add(group)
        Staff.objects.create(
            user=instance,
            username=instance.username,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
        )


post_save.connect(staff_profile, sender=User)

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
