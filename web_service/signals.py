from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserLogSettings

@receiver(post_save, sender=User)
def create_user_log_settings(sender, instance, created, **kwargs):
    if created:
        UserLogSettings.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_log_settings(sender, instance, **kwargs):
    if hasattr(instance, 'log_settings'):
        instance.log_settings.save()