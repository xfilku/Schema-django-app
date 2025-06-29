from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserLogSettings, UserSilentSettings


@receiver(post_save, sender=User)
def manage_user_settings(sender, instance, created, **kwargs):
    """
    Tworzy domyślne ustawienia logów i list paginacyjnych dla nowego użytkownika.
    Przy aktualizacji zapisuje istniejące ustawienia.
    """
    if created:
        UserLogSettings.objects.create(user=instance)
        UserSilentSettings.objects.create(user=instance)
    else:
        if hasattr(instance, 'log_settings'):
            instance.log_settings.save()
        if hasattr(instance, 'list_settings'):
            instance.list_settings.save()
