from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import UserPreferences


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_preferences(sender, instance, created, **kwargs):
    if created:
        UserPreferences.objects.create(user=instance)
        instance.userpreferences.save()


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def save_preferences(sender, instance, created, **kwargs):
#     if created:
#         instance.userpreferences.save()
