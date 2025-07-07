"""
Comprehensive test suite for the backend app
Tests models, business logic, and API endpoints
"""

import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from unittest.mock import patch, MagicMock

from .models import Credentials, SecureNote, ActivityLog, EncryptionMixin
from .forms import CredentialForm, SecureNoteForm, SearchForm
from .business_logic import (
    CredentialsManager, SecureNotesManager, DashboardManager,
    ActivityManager, SearchManager, DataExportManager,
    FavoriteManager, AccessTracker
)


class EncryptionMixinTestCase(TestCase):
    """Test encryption/decryption functionality"""
    
    def test_encryption_key_generation(self):
        """Test that encryption key is generated consistently"""
        key1 = EncryptionMixin.get_encryption_key()
        key2 = EncryptionMixin.get_encryption_key()
        self.assertEqual(key1, key2)
        self.assertIsInstance(key1, bytes)
    
    def test_data_encryption_decryption(self):
        """Test data can be encrypted and decrypted"""
        original_text = "sensitive_password123"
        encrypted = EncryptionMixin.encrypt_data(original_text)
        decrypted = EncryptionMixin.decrypt_data(encrypted)
        
        self.assertNotEqual(original_text, encrypted)
        self.assertEqual(original_text, decrypted)
    
    def test_empty_data_handling(self):
        """Test handling of empty data"""
        self.assertEqual(EncryptionMixin.encrypt_data(""), "")
        self.assertEqual(EncryptionMixin.encrypt_data(None), None)
        self.assertEqual(EncryptionMixin.decrypt_data(""), "")
        self.assertEqual(EncryptionMixin.decrypt_data(None), None)
    
    def test_invalid_encrypted_data(self):
        """Test handling of invalid encrypted data"""
        result = EncryptionMixin.decrypt_data("invalid_encrypted_data")
        self.assertEqual(result, "[Decryption Error]")


class CredentialsModelTestCase(TestCase):
    """Test Credentials model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
    
    def test_credential_creation(self):
        """Test creating a credential"""
        credential = Credentials.objects.create(
            user=self.user,
            label="Test Gmail",
            type="email",
            website_url="https://gmail.com",
            username="testuser@gmail.com",
            password_encrypted="encrypted_password_data",
            note="Test note"
        )
        
        self.assertEqual(credential.user, self.user)
        self.assertEqual(credential.label, "Test Gmail")
        self.assertEqual(credential.type, "email")
        self.assertFalse(credential.is_favorite)
    
    def test_password_property(self):
        """Test password encryption/decryption property"""
        credential = Credentials.objects.create(
            user=self.user,
            label="Test Service",
        )
        
        # Test setting password
        test_password = "my_secret_password"
        credential.password = test_password
        credential.save()
        
        # Test getting password
        retrieved_credential = Credentials.objects.get(pk=credential.pk)
        self.assertEqual(retrieved_credential.password, test_password)
    
    def test_secret_key_property(self):
        """Test secret key encryption/decryption property"""
        credential = Credentials.objects.create(
            user=self.user,
            label="Test Service",
        )
        
        # Test setting secret key
        test_secret = "ABCD1234567890"
        credential.secret_key = test_secret
        credential.save()
        
        # Test getting secret key
        retrieved_credential = Credentials.objects.get(pk=credential.pk)
        self.assertEqual(retrieved_credential.secret_key, test_secret)
    
    def test_get_tags_list(self):
        """Test tags list parsing"""
        credential = Credentials.objects.create(
            user=self.user,
            label="Test Service",
            tags="work, important, email"
        )
        
        tags = credential.get_tags_list()
        self.assertEqual(tags, ['work', 'important', 'email'])
        
        # Test empty tags
        credential.tags = ""
        self.assertEqual(credential.get_tags_list(), [])
        
        credential.tags = None
        self.assertEqual(credential.get_tags_list(), [])
    
    def test_get_type_icon(self):
        """Test type icon mapping"""
        credential = Credentials.objects.create(
            user=self.user,
            label="Test Service",
            type="email"
        )
        
        self.assertEqual(credential.get_type_icon(), "fas fa-envelope")
        
        credential.type = "unknown_type"
        self.assertEqual(credential.get_type_icon(), "fas fa-folder")
    
    def test_str_representation(self):
        """Test string representation"""
        credential = Credentials.objects.create(
            user=self.user,
            label="Test Gmail",
            type="email"
        )
        
        self.assertEqual(str(credential), "Test Gmail (email)")


class SecureNoteModelTestCase(TestCase):
    """Test SecureNote model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
    
    def test_note_creation(self):
        """Test creating a secure note"""
        note = SecureNote.objects.create(
            user=self.user,
            title="Important Note",
            content_encrypted="encrypted_content_data",
            type="personal"
        )
        
        self.assertEqual(note.user, self.user)
        self.assertEqual(note.title, "Important Note")
        self.assertEqual(note.type, "personal")
        self.assertFalse(note.is_favorite)
    
    def test_content_property(self):
        """Test content encryption/decryption property"""
        note = SecureNote.objects.create(
            user=self.user,
            title="Test Note"
        )
        
        # Test setting content
        test_content = "This is sensitive information"
        note.content = test_content
        note.save()
        
        # Test getting content
        retrieved_note = SecureNote.objects.get(pk=note.pk)
        self.assertEqual(retrieved_note.content, test_content)
    
    def test_get_type_icon(self):
        """Test type icon mapping"""
        note = SecureNote.objects.create(
            user=self.user,
            title="Test Note",
            type="work"
        )
        
        self.assertEqual(note.get_type_icon(), "fas fa-briefcase")
        
        note.type = "unknown_type"
        self.assertEqual(note.get_type_icon(), "fas fa-sticky-note")


class ActivityLogModelTestCase(TestCase):
    """Test ActivityLog model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
    
    def test_activity_log_creation(self):
        """Test creating an activity log"""
        activity = ActivityLog.objects.create(
            user=self.user,
            action="login",
            description="User logged in",
            ip_address="192.168.1.1"
        )
        
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.action, "login")
        self.assertEqual(activity.description, "User logged in")
        self.assertEqual(activity.ip_address, "192.168.1.1")
    
    def test_str_representation(self):
        """Test string representation"""
        activity = ActivityLog.objects.create(
            user=self.user,
            action="login",
            description="User logged in"
        )
        
        expected = f"testuser - login at {activity.timestamp}"
        self.assertEqual(str(activity), expected)


class CredentialsManagerTestCase(TestCase):
    """Test CredentialsManager business logic"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Create test credentials
        self.credential1 = Credentials.objects.create(
            user=self.user,
            label="Gmail Account",
            type="email",
            username="test@gmail.com",
            is_favorite=True
        )
        
        self.credential2 = Credentials.objects.create(
            user=self.user,
            label="GitHub Account",
            type="website",
            username="testuser"
        )
    
    def test_get_user_credentials(self):
        """Test getting user credentials"""
        credentials = CredentialsManager.get_user_credentials(self.user)
        self.assertEqual(credentials.count(), 2)
    
    def test_get_user_credentials_with_search(self):
        """Test getting credentials with search parameters"""
        search_params = {
            'query': 'Gmail',
            'type_filter': 'email',
            'favorites_only': True
        }
        
        credentials = CredentialsManager.get_user_credentials(self.user, search_params)
        self.assertEqual(credentials.count(), 1)
        self.assertEqual(credentials.first().label, "Gmail Account")
    
    def test_create_credential(self):
        """Test creating a credential"""
        form_data = {
            'label': 'New Service',
            'type': 'website',
            'username': 'newuser',
            'password': 'newpassword'
        }
        
        credential, errors = CredentialsManager.create_credential(self.user, form_data)
        
        self.assertIsNotNone(credential)
        self.assertIsNone(errors)
        self.assertEqual(credential.label, 'New Service')
        self.assertEqual(credential.user, self.user)
    
    def test_update_credential(self):
        """Test updating a credential"""
        form_data = {
            'label': 'Updated Gmail',
            'type': 'email',
            'username': 'updated@gmail.com'
        }
        
        credential, errors = CredentialsManager.update_credential(self.credential1, form_data)
        
        self.assertIsNotNone(credential)
        self.assertIsNone(errors)
        self.assertEqual(credential.label, 'Updated Gmail')
    
    def test_delete_credential(self):
        """Test deleting a credential"""
        credential_label = CredentialsManager.delete_credential(self.credential1)
        
        self.assertEqual(credential_label, "Gmail Account")
        self.assertFalse(Credentials.objects.filter(pk=self.credential1.pk).exists())


class DashboardManagerTestCase(TestCase):
    """Test DashboardManager business logic"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Create test data
        Credentials.objects.create(
            user=self.user,
            label="Test Credential",
            type="email",
            is_favorite=True
        )
        
        SecureNote.objects.create(
            user=self.user,
            title="Test Note",
            type="personal",
            is_favorite=True
        )
        
        ActivityLog.objects.create(
            user=self.user,
            action="login",
            description="User logged in"
        )
    
    def test_get_dashboard_stats(self):
        """Test getting dashboard statistics"""
        stats = DashboardManager.get_dashboard_stats(self.user)
        
        self.assertEqual(stats['total_credentials'], 1)
        self.assertEqual(stats['total_notes'], 1)
        self.assertEqual(stats['favorite_credentials'], 1)
        self.assertEqual(stats['favorite_notes'], 1)
        self.assertEqual(len(stats['recent_activities']), 1)
        self.assertEqual(len(stats['recent_credentials']), 1)
        self.assertEqual(len(stats['recent_notes']), 1)


class ActivityManagerTestCase(TestCase):
    """Test ActivityManager business logic"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
    
    def test_log_activity(self):
        """Test logging an activity"""
        activity = ActivityManager.log_activity(
            self.user, 
            'create_credential', 
            'Created test credential'
        )
        
        self.assertIsNotNone(activity)
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.action, 'create_credential')
        self.assertEqual(activity.description, 'Created test credential')
    
    def test_get_user_activities(self):
        """Test getting user activities"""
        # Create test activities
        ActivityManager.log_activity(self.user, 'login', 'User logged in')
        ActivityManager.log_activity(self.user, 'logout', 'User logged out')
        
        activities = ActivityManager.get_user_activities(self.user, 1)
        self.assertEqual(len(activities), 1)


class FavoriteManagerTestCase(TestCase):
    """Test FavoriteManager business logic"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        self.credential = Credentials.objects.create(
            user=self.user,
            label="Test Credential",
            is_favorite=False
        )
    
    def test_toggle_favorite(self):
        """Test toggling favorite status"""
        # Toggle to favorite
        is_favorite = FavoriteManager.toggle_favorite(self.credential, self.user)
        self.assertTrue(is_favorite)
        
        # Refresh from database
        self.credential.refresh_from_db()
        self.assertTrue(self.credential.is_favorite)
        
        # Toggle back
        is_favorite = FavoriteManager.toggle_favorite(self.credential, self.user)
        self.assertFalse(is_favorite)
    
    def test_get_user_favorites(self):
        """Test getting user favorites"""
        # Make credential favorite
        self.credential.is_favorite = True
        self.credential.save()
        
        favorites = FavoriteManager.get_user_favorites(self.user)
        self.assertEqual(favorites['credentials'].count(), 1)
        self.assertEqual(favorites['notes'].count(), 0)


class FormsTestCase(TestCase):
    """Test form validation and functionality"""
    
    def test_credential_form_valid(self):
        """Test valid credential form"""
        form_data = {
            'label': 'Test Service',
            'type': 'website',
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'test@example.com'
        }
        
        form = CredentialForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_credential_form_password_validation(self):
        """Test password validation"""
        form_data = {
            'label': 'Test Service',
            'type': 'website',
            'password': 'short'  # Too short
        }
        
        form = CredentialForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
    
    def test_secure_note_form_valid(self):
        """Test valid secure note form"""
        form_data = {
            'title': 'Test Note',
            'content': 'This is test content',
            'type': 'personal'
        }
        
        form = SecureNoteForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_search_form_valid(self):
        """Test search form"""
        form_data = {
            'query': 'test search',
            'type_filter': 'email',
            'favorites_only': True
        }
        
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class APIEndpointsTestCase(TestCase):
    """Test API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpassword123')
        
        # Create test data
        self.credential = Credentials.objects.create(
            user=self.user,
            label="Test Credential",
            type="email"
        )
    
    def test_api_user_stats(self):
        """Test user stats API endpoint"""
        url = reverse('backend:api_user_stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('total_credentials', data)
        self.assertEqual(data['total_credentials'], 1)
    
    def test_api_toggle_favorite(self):
        """Test toggle favorite API endpoint"""
        url = reverse('backend:api_toggle_favorite')
        data = {
            'type': 'credential',
            'id': self.credential.pk
        }
        
        response = self.client.post(
            url, 
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertTrue(response_data['is_favorite'])
    
    def test_api_search(self):
        """Test search API endpoint"""
        url = reverse('backend:api_search')
        data = {
            'query': 'Test',
            'type_filter': 'email',
            'favorites_only': False
        }
        
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('credentials', response_data)
        self.assertEqual(response_data['total_credentials'], 1)
    
    def test_api_requires_authentication(self):
        """Test that API endpoints require authentication"""
        self.client.logout()
        
        url = reverse('backend:api_user_stats')
        response = self.client.get(url)
        
        # Should redirect to login
        self.assertEqual(response.status_code, 302)


class IntegrationTestCase(TestCase):
    """Integration tests for the complete backend system"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
    
    def test_complete_credential_workflow(self):
        """Test complete credential management workflow"""
        # Create credential
        form_data = {
            'label': 'Test Gmail',
            'type': 'email',
            'username': 'test@gmail.com',
            'password': 'supersecret123',
            'email': 'test@gmail.com'
        }
        
        credential, errors = CredentialsManager.create_credential(self.user, form_data)
        self.assertIsNotNone(credential)
        
        # Log activity
        activity = ActivityManager.log_activity(
            self.user, 
            'create_credential',
            f'Created credential: {credential.label}'
        )
        self.assertIsNotNone(activity)
        
        # Update access time
        AccessTracker.update_access_time(credential, self.user)
        credential.refresh_from_db()
        self.assertIsNotNone(credential.last_accessed)
        
        # Toggle favorite
        is_favorite = FavoriteManager.toggle_favorite(credential, self.user)
        self.assertTrue(is_favorite)
        
        # Search for it
        search_results = SearchManager.search_all_user_data(
            self.user, 
            query='Gmail'
        )
        self.assertEqual(search_results['total_credentials'], 1)
        
        # Get dashboard stats
        stats = DashboardManager.get_dashboard_stats(self.user)
        self.assertEqual(stats['total_credentials'], 1)
        self.assertEqual(stats['favorite_credentials'], 1)
        
        # Delete credential
        label = CredentialsManager.delete_credential(credential)
        self.assertEqual(label, 'Test Gmail')
        self.assertFalse(Credentials.objects.filter(pk=credential.pk).exists())


class PerformanceTestCase(TestCase):
    """Performance tests for business logic"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Create multiple credentials for performance testing
        for i in range(50):
            Credentials.objects.create(
                user=self.user,
                label=f"Test Credential {i}",
                type="email",
                username=f"user{i}@example.com"
            )
    
    def test_dashboard_stats_performance(self):
        """Test dashboard stats calculation performance"""
        import time
        
        start_time = time.time()
        stats = DashboardManager.get_dashboard_stats(self.user)
        end_time = time.time()
        
        # Should complete within 1 second
        self.assertLess(end_time - start_time, 1.0)
        self.assertEqual(stats['total_credentials'], 50)
    
    def test_search_performance(self):
        """Test search performance with large dataset"""
        import time
        
        start_time = time.time()
        results = SearchManager.search_all_user_data(self.user, query='Test')
        end_time = time.time()
        
        # Should complete within 1 second
        self.assertLess(end_time - start_time, 1.0)
        self.assertEqual(results['total_credentials'], 50)
