from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings
import base64
import hashlib

class EncryptionMixin:
    """Mixin to handle encryption/decryption of sensitive data"""
    
    @staticmethod
    def get_encryption_key():
        """Generate encryption key based on Django secret key"""
        key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
        return base64.urlsafe_b64encode(key)
    
    @classmethod
    def encrypt_data(cls, data):
        """Encrypt sensitive data"""
        if not data:
            return data
        f = Fernet(cls.get_encryption_key())
        return f.encrypt(data.encode()).decode()
    
    @classmethod
    def decrypt_data(cls, encrypted_data):
        """Decrypt sensitive data"""
        if not encrypted_data:
            return encrypted_data
        try:
            f = Fernet(cls.get_encryption_key())
            return f.decrypt(encrypted_data.encode()).decode()
        except:
            return "[Decryption Error]"

class Credentials(models.Model, EncryptionMixin):
    CREDENTIAL_TYPES = [
        ('website', 'Website/App'),
        ('email', 'Email Account'),
        ('social', 'Social Media'),
        ('banking', 'Banking/Finance'),
        ('work', 'Work Related'),
        ('personal', 'Personal'),
        ('server', 'Server/Database'),
        ('api', 'API Key'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credentials')
    label = models.CharField(max_length=255, help_text="Descriptive name for this credential")
    type = models.CharField(max_length=50, choices=CREDENTIAL_TYPES, default='other')
    website_url = models.URLField(blank=True, null=True, help_text="Website URL if applicable")
    
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    password_encrypted = models.TextField(help_text="Encrypted password")
    secret_key_encrypted = models.TextField(blank=True, null=True, help_text="Encrypted secret key or 2FA")
    
    note = models.TextField(blank=True, null=True, help_text="Additional notes")
    is_favorite = models.BooleanField(default=False)
    tags = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated tags")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_accessed = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name_plural = "Credentials"

    def __str__(self):
        return f"{self.label} ({self.type})"
    
    @property
    def password(self):
        """Decrypt and return password"""
        return self.decrypt_data(self.password_encrypted) if self.password_encrypted else ""
    
    @password.setter
    def password(self, value):
        """Encrypt and store password"""
        self.password_encrypted = self.encrypt_data(value) if value else ""
    
    @property
    def secret_key(self):
        """Decrypt and return secret key"""
        return self.decrypt_data(self.secret_key_encrypted) if self.secret_key_encrypted else ""
    
    @secret_key.setter
    def secret_key(self, value):
        """Encrypt and store secret key"""
        self.secret_key_encrypted = self.encrypt_data(value) if value else ""
    
    def get_tags_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []
    
    def get_type_icon(self):
        """Return appropriate icon for credential type"""
        icons = {
            'website': 'fas fa-globe',
            'email': 'fas fa-envelope',
            'social': 'fab fa-twitter',
            'banking': 'fas fa-university',
            'work': 'fas fa-briefcase',
            'personal': 'fas fa-user',
            'server': 'fas fa-server',
            'api': 'fas fa-key',
            'other': 'fas fa-folder',
        }
        return icons.get(self.type, 'fas fa-folder')

class SecureNote(models.Model, EncryptionMixin):
    NOTE_TYPES = [
        ('personal', 'Personal'),
        ('work', 'Work'),
        ('financial', 'Financial'),
        ('medical', 'Medical'),
        ('legal', 'Legal'),
        ('technical', 'Technical'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='secure_notes')
    title = models.CharField(max_length=255)
    content_encrypted = models.TextField(help_text="Encrypted note content")
    type = models.CharField(max_length=50, choices=NOTE_TYPES, default='personal')
    
    is_favorite = models.BooleanField(default=False)
    tags = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated tags")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_accessed = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name_plural = "Secure Notes"

    def __str__(self):
        return self.title
    
    @property
    def content(self):
        """Decrypt and return content"""
        return self.decrypt_data(self.content_encrypted) if self.content_encrypted else ""
    
    @content.setter
    def content(self, value):
        """Encrypt and store content"""
        self.content_encrypted = self.encrypt_data(value) if value else ""
    
    def get_tags_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []
    
    def get_type_icon(self):
        """Return appropriate icon for note type"""
        icons = {
            'personal': 'fas fa-user',
            'work': 'fas fa-briefcase',
            'financial': 'fas fa-dollar-sign',
            'medical': 'fas fa-heartbeat',
            'legal': 'fas fa-gavel',
            'technical': 'fas fa-code',
            'other': 'fas fa-sticky-note',
        }
        return icons.get(self.type, 'fas fa-sticky-note')

class ActivityLog(models.Model):
    """Track user activities for security purposes"""
    ACTION_TYPES = [
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('create_credential', 'Created Credential'),
        ('view_credential', 'Viewed Credential'),
        ('update_credential', 'Updated Credential'),
        ('delete_credential', 'Deleted Credential'),
        ('create_note', 'Created Note'),
        ('view_note', 'Viewed Note'),
        ('update_note', 'Updated Note'),
        ('delete_note', 'Deleted Note'),
        ('export_data', 'Exported Data'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=50, choices=ACTION_TYPES)
    description = models.CharField(max_length=500)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"