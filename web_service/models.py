from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField

class UserLogSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='log_settings')

    log_info = models.BooleanField(default=True)
    log_warning = models.BooleanField(default=True)
    log_error = models.BooleanField(default=True)

    def __str__(self):
        return f"Log settings for {self.user.username}"
    
class UserSilentSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    per_page = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f"Ustawienia {self.user.username}"

class Log(models.Model):
    class LogType(models.TextChoices):
        INFO = 'INFO', 'Informacja'
        WARNING = 'WARNING', 'Ostrzeżenie'
        ERROR = 'ERROR', 'Błąd'

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    action = models.TextField()
    type = models.CharField(
        max_length=9,
        choices=LogType.choices,
        default=LogType.INFO,
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} - {self.user} - {self.action}" 

class FavoriteLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7)

    def __str__(self):
        return f"{self.name}"
    
class InfoServiceConfiguration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="info_page_configuration")
    log_display_limit = models.PositiveSmallIntegerField(default=3)
    announcement_display_limit = models.PositiveSmallIntegerField(default=1)

    ticket_display_switch = models.BooleanField(default=True)
    logs_disaply_switch = models.BooleanField(default=True)
    announcement_display_switch = models.BooleanField(default=True)
    fast_settings_display_switch = models.BooleanField(default=True)

    def __str__(self):
        return f"Konfiguracja infoserwisu dla {self.user.username}"
    
class Announcement(models.Model):
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    subject = models.CharField(max_length=75)
    message = models.TextField(max_length=350)

    def __str__(self):
        return f"{self.subject} ({self.date})"
    
class UserPermissions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_permissions')
    permissions = JSONField(default=dict)  # np. {"announcement.view": true, ...}

    def has_permission(self, code):
        return self.permissions.get(code, False)

    def __str__(self):
        return f"Uprawnienia {self.user.username}"
