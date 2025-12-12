from .models import UserAPIKey
from django import forms

class UserAPIKeyForm(forms.ModelForm):
    api_key = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your OpenAI API key...', 'class': 'form-control'}))

    class Meta:
        model = UserAPIKey
        fields = []  # Don't use model fields directly

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        instance.api_key = self.cleaned_data['api_key']
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class AccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with that email already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data

from .models import UserProfile
from .models import Country

class UserProfileForm(forms.ModelForm):
    country = forms.ChoiceField(choices=[], required=True)
    institution_name = forms.CharField(max_length=200, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].choices = [(c.name, c.name) for c in Country.objects.order_by('name')]
        self.fields['country'].widget.attrs.update({
            'class': 'form-select',
            'id': 'country',
            'required': 'required',
        })
        self.fields['institution_name'].widget.attrs.update({
            'class': 'form-control',
            'id': 'institution_name',
            'required': 'required',
        })

    class Meta:
        model = UserProfile
        fields = ['country', 'state', 'career_stage', 'institution_name', 'discipline', 'ai_consent']
