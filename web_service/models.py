from django.db import models
from django.contrib.auth.models import User

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
    