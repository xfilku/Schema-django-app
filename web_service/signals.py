"""
Signal handlers for automatic user configuration setup.

These signals initialize default settings (log visibility, pagination,
and permissions) when a new User instance is created.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserLogSettings, UserSilentSettings, UserPermissions


@receiver(post_save, sender=User)
def manage_user_settings(sender, instance, created, **kwargs):
    """
    Creates default log and pagination settings for new users.

    If the user already exists (updated), saves existing settings if present.

    Args:
        sender (Model): The model class (User).
        instance (User): The actual user instance.
        created (bool): Whether this was a creation or update.
    """
    if created:
        UserLogSettings.objects.create(user=instance)
        UserSilentSettings.objects.create(user=instance)
    else:
        if hasattr(instance, 'log_settings'):
            instance.log_settings.save()
        if hasattr(instance, 'list_settings'):
            instance.list_settings.save()


@receiver(post_save, sender=User)
def create_user_permissions(sender, instance, created, **kwargs):
    """
    Creates a default UserPermissions instance for new users.

    Ensures every user has a permissions container on creation.
    """
    if created and not hasattr(instance, 'custom_permissions'):
        UserPermissions.objects.create(user=instance)
