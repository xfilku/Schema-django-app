# forms.py
from .models import Tag, PhoneContact
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

class PhoneContactForm(forms.ModelForm):
    class Meta:
        model = PhoneContact
        fields = [
            'company_name',
            'nip',
            'city',
            'phone_number',
            'status',
            'tag',
            'note',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('company_name', css_class='form-group col-md-6 mb-0'),
                Column('nip', css_class='form-group col-md-6 mb-0'),
                css_class='row'
            ),
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
                css_class='row'
            ),
            Row(
                Column('status', css_class='form-group col-md-6 mb-0'),
                Column('tag', css_class='form-group col-md-6 mb-0'),
                css_class='row'
            ),
            'note',
            Submit('submit', 'Zapisz', css_class='btn btn-primary')
        )