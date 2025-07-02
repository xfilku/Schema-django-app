# forms.py
from .models import Tag, InfoServiceConfiguration, Announcement, UserLogSettings
from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils import timezone

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Inicjuj helpera crispy-forms
        self.helper = FormHelper()
        self.helper.form_method = 'post'

class TagAdminForm(forms.ModelForm):
    color = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color'}),
        label="Kolor flagi"
    )

    class Meta:
        model = Tag
        fields = '__all__'

class TagForm(forms.ModelForm):
    color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))

    class Meta:
        model = Tag
        fields = ['name', 'color']

class InfoServiceConfigurationForm(forms.ModelForm):
    class Meta:
        model = InfoServiceConfiguration
        fields = [
            'log_display_limit',
            'announcement_display_limit',
            'ticket_display_switch',
            'logs_disaply_switch',
            'announcement_display_switch',
            'fast_settings_display_switch'
        ]
        labels = {
            'log_display_limit': "Ilość logów",
            'announcement_display_limit': "Ilość ogłoszeń",
            'ticket_display_switch': "Pokazuj zgłoszenia",
            'logs_disaply_switch': "Pokazuj logi",
            'announcement_display_switch': "Pokazuj ogłoszenia",
            'fast_settings_display_switch': "Pokazuj szybkie ustawienia"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['date', 'subject', 'message']
        labels = {
            'date': 'Data ogłoszenia',
            'subject': 'Temat',
            'message': 'Treść'
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.now().date()
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Dodaj ogłoszenie', css_class='btn btn-success'))

class CustomUserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)

    # Pola z UserLogSettings
    log_info = forms.BooleanField(label='Loguj INFO', required=False, initial=True)
    log_warning = forms.BooleanField(label='Loguj WARNING', required=False, initial=True)
    log_error = forms.BooleanField(label='Loguj ERROR', required=False, initial=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Zapisz', css_class='btn btn-success'))

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            self.add_error('password2', "Hasła muszą być takie same.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            # Tworzymy log settings
            UserLogSettings.objects.create(
                user=user,
                log_info=self.cleaned_data.get('log_info', True),
                log_warning=self.cleaned_data.get('log_warning', True),
                log_error=self.cleaned_data.get('log_error', True),
            )
        return user


class CustomUserEditForm(forms.ModelForm):
    # Pola z UserLogSettings
    log_info = forms.BooleanField(label='Loguj INFO', required=False)
    log_warning = forms.BooleanField(label='Loguj WARNING', required=False)
    log_error = forms.BooleanField(label='Loguj ERROR', required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        # Wstępne dane z UserLogSettings
        if instance and hasattr(instance, 'log_settings'):
            self.fields['log_info'].initial = instance.log_settings.log_info
            self.fields['log_warning'].initial = instance.log_settings.log_warning
            self.fields['log_error'].initial = instance.log_settings.log_error

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Zapisz', css_class='btn btn-success'))

    def save(self, commit=True):
        user = super().save(commit)
        # aktualizacja log settings
        if hasattr(user, 'log_settings'):
            user.log_settings.log_info = self.cleaned_data.get('log_info', False)
            user.log_settings.log_warning = self.cleaned_data.get('log_warning', False)
            user.log_settings.log_error = self.cleaned_data.get('log_error', False)
            user.log_settings.save()
        return user