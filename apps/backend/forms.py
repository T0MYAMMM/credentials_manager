from django import forms
from .models import Credentials, SecureNote
import re

class CredentialForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }),
        required=False,
        help_text="Leave blank to keep current password"
    )
    
    secret_key = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Secret Key / 2FA'
        }),
        required=False,
        help_text="Optional: Secret key or 2FA backup codes"
    )

    class Meta:
        model = Credentials
        fields = ['label', 'type', 'website_url', 'username', 'email', 'password', 'secret_key', 'note', 'is_favorite', 'tags']
        widgets = {
            'label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Gmail Account, GitHub, etc.'
            }),
            'type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'website_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Additional notes...'
            }),
            'is_favorite': forms.CheckboxInput(attrs={
                'class': 'custom-control-input'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'work, personal, important (comma-separated)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing existing credential, populate password field
        if self.instance and self.instance.pk:
            self.fields['password'].widget.attrs['placeholder'] = 'Current password (hidden)'

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) < 8:
            raise forms.ValidationError("Password should be at least 8 characters long for security.")
        return password

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        if tags:
            # Clean and validate tags
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            if len(tag_list) > 10:
                raise forms.ValidationError("Maximum 10 tags allowed.")
            return ', '.join(tag_list)
        return tags

    def save(self, commit=True):
        credential = super().save(commit=False)
        
        # Handle password encryption
        password = self.cleaned_data.get('password')
        if password:
            credential.password = password
        
        # Handle secret key encryption
        secret_key = self.cleaned_data.get('secret_key')
        if secret_key:
            credential.secret_key = secret_key
        
        if commit:
            credential.save()
        return credential

class SecureNoteForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Your secure note content...'
        }),
        help_text="This content will be encrypted and stored securely"
    )

    class Meta:
        model = SecureNote
        fields = ['title', 'content', 'type', 'is_favorite', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Note title'
            }),
            'type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_favorite': forms.CheckboxInput(attrs={
                'class': 'custom-control-input'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'work, personal, important (comma-separated)'
            }),
        }

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        if tags:
            # Clean and validate tags
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            if len(tag_list) > 10:
                raise forms.ValidationError("Maximum 10 tags allowed.")
            return ', '.join(tag_list)
        return tags

    def save(self, commit=True):
        note = super().save(commit=False)
        
        # Handle content encryption
        content = self.cleaned_data.get('content')
        if content:
            note.content = content
        
        if commit:
            note.save()
        return note

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search credentials and notes...',
            'autocomplete': 'off'
        }),
        required=False
    )
    
    type_filter = forms.ChoiceField(
        choices=[('all', 'All Types')] + Credentials.CREDENTIAL_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        required=False,
        initial='all'
    )
    
    favorites_only = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'custom-control-input'
        }),
        required=False
    ) 