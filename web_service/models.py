from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserLogSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='log_settings')

    log_info = models.BooleanField(default=True)
    log_warning = models.BooleanField(default=True)
    log_error = models.BooleanField(default=True)

    def __str__(self):
        return f"Log settings for {self.user.username}"

class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7)

    def __str__(self):
        return f"{self.name}"
    
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
    
    
class ContactStatus(models.TextChoices):
    NEW = 'new', 'Nowy'
    CALLBACK = 'callback', 'Do ponownego kontaktu'
    PASSED_TO_DEV = 'passed', 'Przekazany programiście'
    REJECTED = 'rejected', 'Odrzucony'
    OTHER = 'other', 'Inne'

class PhoneContact(models.Model):
    company_name = models.CharField(max_length=255)
    nip = models.CharField(max_length=10, verbose_name="NIP")
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    
    status = models.CharField(
        max_length=20,
        choices=ContactStatus.choices,
        default=ContactStatus.NEW
    )
    note = models.TextField(blank=True, null=True)

    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    contact_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-contact_date']

    def __str__(self):
        return f"{self.company_name} ({self.phone_number}) - {self.get_status_display()}"