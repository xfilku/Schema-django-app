# forms.py
from .models import Tag
from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column

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
