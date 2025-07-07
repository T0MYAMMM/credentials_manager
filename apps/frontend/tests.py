"""
Frontend Tests for Credentials Manager
Tests frontend views, templates, and UI functionality
"""

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from django.http import JsonResponse
from unittest.mock import patch, MagicMock

from apps.backend.models import Credentials, SecureNote, ActivityLog
from apps.backend.business_logic import (
    CredentialsManager, SecureNotesManager, DashboardManager,
    ActivityManager
)


class FrontendViewsTestCase(TestCase):
    """Test frontend view functionality"""
    
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
            label="Test Gmail",
            type="email",
            username="test@gmail.com"
        )
        
        self.note = SecureNote.objects.create(
            user=self.user,
            title="Test Note",
            type="personal"
        )
    
    def test_dashboard_view(self):
        """Test dashboard page loads correctly"""
        url = reverse('frontend:dashboard')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
        self.assertContains(response, 'Total Credentials')
        self.assertContains(response, 'Secure Notes')
    
    def test_dashboard_context(self):
        """Test dashboard context data"""
        url = reverse('frontend:dashboard')
        response = self.client.get(url)
        
        context = response.context
        self.assertIn('total_credentials', context)
        self.assertIn('total_notes', context)
        self.assertEqual(context['total_credentials'], 1)
        self.assertEqual(context['total_notes'], 1)
    
    def test_credentials_list_view(self):
        """Test credentials list page"""
        url = reverse('frontend:credentials_list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Credentials')
        self.assertContains(response, 'Test Gmail')
    
    def test_credentials_list_search(self):
        """Test credentials list with search"""
        url = reverse('frontend:credentials_list')
        response = self.client.get(url, {'query': 'Gmail'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Gmail')
        
        # Test no results
        response = self.client.get(url, {'query': 'NonExistent'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No Credentials Found')
    
    def test_credential_detail_view(self):
        """Test credential detail page"""
        url = reverse('frontend:credential_detail', kwargs={'pk': self.credential.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Gmail')
        self.assertContains(response, 'test@gmail.com')
    
    def test_credential_detail_access_tracking(self):
        """Test that credential detail view updates access time"""
        # Check initial state
        self.assertIsNone(self.credential.last_accessed)
        
        url = reverse('frontend:credential_detail', kwargs={'pk': self.credential.pk})
        self.client.get(url)
        
        # Refresh from database
        self.credential.refresh_from_db()
        self.assertIsNotNone(self.credential.last_accessed)
    
    def test_credential_create_get(self):
        """Test credential create form display"""
        url = reverse('frontend:credential_create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add New Credential')
        self.assertContains(response, 'form')
    
    def test_credential_create_post_valid(self):
        """Test credential creation with valid data"""
        url = reverse('frontend:credential_create')
        data = {
            'label': 'New Service',
            'type': 'website',
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'new@example.com'
        }
        
        response = self.client.post(url, data)
        
        # Should redirect to detail page
        self.assertEqual(response.status_code, 302)
        
        # Check credential was created
        new_credential = Credentials.objects.filter(label='New Service').first()
        self.assertIsNotNone(new_credential)
        self.assertEqual(new_credential.user, self.user)
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('created successfully' in str(m) for m in messages))
    
    def test_credential_create_post_invalid(self):
        """Test credential creation with invalid data"""
        url = reverse('frontend:credential_create')
        data = {
            'label': '',  # Required field missing
            'type': 'website'
        }
        
        response = self.client.post(url, data)
        
        # Should stay on form page
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add New Credential')
    
    def test_credential_edit_get(self):
        """Test credential edit form display"""
        url = reverse('frontend:credential_edit', kwargs={'pk': self.credential.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Test Gmail')
        self.assertContains(response, 'test@gmail.com')
    
    def test_credential_edit_post_valid(self):
        """Test credential update with valid data"""
        url = reverse('frontend:credential_edit', kwargs={'pk': self.credential.pk})
        data = {
            'label': 'Updated Gmail',
            'type': 'email',
            'username': 'updated@gmail.com'
        }
        
        response = self.client.post(url, data)
        
        # Should redirect to detail page
        self.assertEqual(response.status_code, 302)
        
        # Check credential was updated
        self.credential.refresh_from_db()
        self.assertEqual(self.credential.label, 'Updated Gmail')
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('updated successfully' in str(m) for m in messages))
    
    def test_credential_delete(self):
        """Test credential deletion"""
        url = reverse('frontend:credential_delete', kwargs={'pk': self.credential.pk})
        response = self.client.post(url)
        
        # Should redirect to list page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith(reverse('frontend:credentials_list')))
        
        # Check credential was deleted
        self.assertFalse(Credentials.objects.filter(pk=self.credential.pk).exists())
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('deleted successfully' in str(m) for m in messages))
    
    def test_notes_list_view(self):
        """Test notes list page"""
        url = reverse('frontend:notes_list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Secure Notes')
        self.assertContains(response, 'Test Note')
    
    def test_note_detail_view(self):
        """Test note detail page"""
        url = reverse('frontend:note_detail', kwargs={'pk': self.note.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
    
    def test_note_create_post_valid(self):
        """Test note creation with valid data"""
        url = reverse('frontend:note_create')
        data = {
            'title': 'New Note',
            'content': 'This is new content',
            'type': 'personal'
        }
        
        response = self.client.post(url, data)
        
        # Should redirect to detail page
        self.assertEqual(response.status_code, 302)
        
        # Check note was created
        new_note = SecureNote.objects.filter(title='New Note').first()
        self.assertIsNotNone(new_note)
        self.assertEqual(new_note.user, self.user)
    
    def test_toggle_favorite_ajax(self):
        """Test toggle favorite AJAX endpoint"""
        url = reverse('frontend:toggle_favorite')
        data = {
            'type': 'credential',
            'id': self.credential.pk
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 200)
        
        # Parse JSON response
        import json
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertTrue(response_data['is_favorite'])
        
        # Check credential was updated
        self.credential.refresh_from_db()
        self.assertTrue(self.credential.is_favorite)
    
    def test_export_data(self):
        """Test data export functionality"""
        url = reverse('frontend:export_data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment', response['Content-Disposition'])
    
    def test_search_view(self):
        """Test search page"""
        url = reverse('frontend:search')
        response = self.client.get(url, {'query': 'Gmail'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search')
        # Should show results
        self.assertContains(response, 'Test Gmail')
    
    def test_activity_log_view(self):
        """Test activity log page"""
        # Create an activity log entry
        ActivityLog.objects.create(
            user=self.user,
            action='login',
            description='User logged in'
        )
        
        url = reverse('frontend:activity_log')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Activity Log')
        self.assertContains(response, 'User logged in')


class FrontendPermissionsTestCase(TestCase):
    """Test frontend view permissions and access control"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword123'
        )
        
        self.credential = Credentials.objects.create(
            user=self.user,
            label="Private Credential",
            type="email"
        )
        
        self.client = Client()
    
    def test_unauthenticated_access(self):
        """Test that unauthenticated users are redirected to login"""
        urls_to_test = [
            'frontend:dashboard',
            'frontend:credentials_list',
            'frontend:credential_create',
            'frontend:notes_list',
            'frontend:note_create',
            'frontend:search',
            'frontend:activity_log',
            'frontend:export_data'
        ]
        
        for url_name in urls_to_test:
            url = reverse(url_name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith('/auth/login'))
    
    def test_user_isolation(self):
        """Test that users can only access their own data"""
        # Login as other user
        self.client.login(username='otheruser', password='otherpassword123')
        
        # Try to access first user's credential
        url = reverse('frontend:credential_detail', kwargs={'pk': self.credential.pk})
        response = self.client.get(url)
        
        # Should return 404 (not found) since it's not the user's credential
        self.assertEqual(response.status_code, 404)
    
    def test_credential_edit_permissions(self):
        """Test credential edit permissions"""
        # Login as other user
        self.client.login(username='otheruser', password='otherpassword123')
        
        # Try to edit first user's credential
        url = reverse('frontend:credential_edit', kwargs={'pk': self.credential.pk})
        response = self.client.get(url)
        
        # Should return 404
        self.assertEqual(response.status_code, 404)
    
    def test_credential_delete_permissions(self):
        """Test credential delete permissions"""
        # Login as other user
        self.client.login(username='otheruser', password='otherpassword123')
        
        # Try to delete first user's credential
        url = reverse('frontend:credential_delete', kwargs={'pk': self.credential.pk})
        response = self.client.post(url)
        
        # Should return 404
        self.assertEqual(response.status_code, 404)
        
        # Credential should still exist
        self.assertTrue(Credentials.objects.filter(pk=self.credential.pk).exists())


class FrontendTemplateTestCase(TestCase):
    """Test frontend template functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpassword123')
    
    def test_dashboard_template_context(self):
        """Test dashboard template receives correct context"""
        url = reverse('frontend:dashboard')
        response = self.client.get(url)
        
        # Check template used
        self.assertTemplateUsed(response, 'frontend/dashboard.html')
        
        # Check context variables
        context = response.context
        required_context_vars = [
            'total_credentials', 'total_notes',
            'favorite_credentials', 'favorite_notes',
            'recent_activities', 'recent_credentials', 'recent_notes'
        ]
        
        for var in required_context_vars:
            self.assertIn(var, context)
    
    def test_credentials_list_template(self):
        """Test credentials list template"""
        url = reverse('frontend:credentials_list')
        response = self.client.get(url)
        
        self.assertTemplateUsed(response, 'frontend/credentials_list.html')
        self.assertIn('page_obj', response.context)
        self.assertIn('form', response.context)
    
    def test_credential_form_template(self):
        """Test credential form templates"""
        # Create form
        url = reverse('frontend:credential_create')
        response = self.client.get(url)
        
        self.assertTemplateUsed(response, 'frontend/credential_form.html')
        self.assertIn('form', response.context)
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Add New Credential')


class FrontendPaginationTestCase(TestCase):
    """Test pagination functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpassword123')
        
        # Create many credentials for pagination testing
        for i in range(25):
            Credentials.objects.create(
                user=self.user,
                label=f"Test Credential {i}",
                type="email"
            )
    
    def test_credentials_list_pagination(self):
        """Test credentials list pagination"""
        url = reverse('frontend:credentials_list')
        response = self.client.get(url)
        
        # Check pagination is working
        self.assertIn('page_obj', response.context)
        page_obj = response.context['page_obj']
        
        # Should have multiple pages (default is 12 items per page)
        self.assertTrue(page_obj.has_other_pages())
        self.assertGreater(page_obj.paginator.num_pages, 1)
        
        # Test page 2
        response = self.client.get(url, {'page': 2})
        self.assertEqual(response.status_code, 200)
        page_obj = response.context['page_obj']
        self.assertEqual(page_obj.number, 2)


class FrontendFormErrorsTestCase(TestCase):
    """Test form error handling in frontend"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpassword123')
    
    def test_credential_create_form_errors(self):
        """Test credential creation form error display"""
        url = reverse('frontend:credential_create')
        
        # Submit form with missing required field
        data = {
            'type': 'website',
            # Missing 'label' which is required
        }
        
        response = self.client.post(url, data)
        
        # Should stay on form page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontend/credential_form.html')
        
        # Check form has errors
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('label', form.errors)
    
    def test_note_create_form_errors(self):
        """Test note creation form error display"""
        url = reverse('frontend:note_create')
        
        # Submit form with missing required field
        data = {
            'type': 'personal',
            # Missing 'title' which is required
        }
        
        response = self.client.post(url, data)
        
        # Should stay on form page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontend/note_form.html')
        
        # Check form has errors
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('title', form.errors)


class FrontendBehaviorTestCase(TestCase):
    """Test frontend behavior and user experience"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpassword123')
    
    def test_credential_create_redirect(self):
        """Test that successful credential creation redirects properly"""
        url = reverse('frontend:credential_create')
        data = {
            'label': 'New Test Service',
            'type': 'website',
            'username': 'testuser'
        }
        
        response = self.client.post(url, data)
        
        # Should redirect to detail page
        self.assertEqual(response.status_code, 302)
        
        # Find the created credential
        credential = Credentials.objects.filter(label='New Test Service').first()
        self.assertIsNotNone(credential)
        
        # Check redirect URL
        expected_url = reverse('frontend:credential_detail', kwargs={'pk': credential.pk})
        self.assertTrue(response.url.endswith(expected_url))
    
    def test_search_preserves_pagination(self):
        """Test that search parameters are preserved in pagination"""
        # Create test data
        for i in range(15):
            Credentials.objects.create(
                user=self.user,
                label=f"Gmail Account {i}",
                type="email"
            )
        
        url = reverse('frontend:credentials_list')
        
        # Search with query
        response = self.client.get(url, {'query': 'Gmail', 'page': 1})
        self.assertEqual(response.status_code, 200)
        
        # Check that search results are displayed
        self.assertContains(response, 'Gmail Account')
    
    def test_empty_state_messages(self):
        """Test empty state messages are displayed correctly"""
        # Test empty credentials list
        url = reverse('frontend:credentials_list')
        response = self.client.get(url)
        
        # Should show empty state message
        self.assertContains(response, 'No Credentials Found')
        
        # Test empty search results
        response = self.client.get(url, {'query': 'nonexistent'})
        self.assertContains(response, 'No Credentials Found')


class FrontendContextProcessorsTestCase(TestCase):
    """Test frontend context processors"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpassword123')
        
        # Create test data
        Credentials.objects.create(
            user=self.user,
            label="Test Credential",
            type="email",
            is_favorite=True
        )
    
    def test_global_stats_context_processor(self):
        """Test that global stats are available in templates"""
        url = reverse('frontend:dashboard')
        response = self.client.get(url)
        
        # Check global stats are in context
        self.assertIn('global_stats', response.context)
        global_stats = response.context['global_stats']
        
        self.assertIn('total_credentials', global_stats)
        self.assertEqual(global_stats['total_credentials'], 1)
    
    def test_app_info_context_processor(self):
        """Test that app info is available in templates"""
        url = reverse('frontend:dashboard')
        response = self.client.get(url)
        
        # Check app info is in context
        self.assertIn('app_name', response.context)
        self.assertIn('app_version', response.context)
        self.assertEqual(response.context['app_name'], 'Credentials Manager')


class FrontendIntegrationTestCase(TestCase):
    """Integration tests for frontend functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpassword123')
    
    def test_complete_credential_crud_workflow(self):
        """Test complete CRUD workflow through frontend"""
        # Create credential
        create_url = reverse('frontend:credential_create')
        create_data = {
            'label': 'Integration Test Service',
            'type': 'website',
            'username': 'testuser',
            'password': 'testpass123',
            'website_url': 'https://example.com'
        }
        
        response = self.client.post(create_url, create_data)
        self.assertEqual(response.status_code, 302)
        
        # Find created credential
        credential = Credentials.objects.filter(label='Integration Test Service').first()
        self.assertIsNotNone(credential)
        
        # Read credential (detail view)
        detail_url = reverse('frontend:credential_detail', kwargs={'pk': credential.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Integration Test Service')
        
        # Update credential
        edit_url = reverse('frontend:credential_edit', kwargs={'pk': credential.pk})
        edit_data = {
            'label': 'Updated Integration Test Service',
            'type': 'website',
            'username': 'updateduser'
        }
        
        response = self.client.post(edit_url, edit_data)
        self.assertEqual(response.status_code, 302)
        
        # Verify update
        credential.refresh_from_db()
        self.assertEqual(credential.label, 'Updated Integration Test Service')
        
        # Delete credential
        delete_url = reverse('frontend:credential_delete', kwargs={'pk': credential.pk})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        
        # Verify deletion
        self.assertFalse(Credentials.objects.filter(pk=credential.pk).exists())
    
    def test_search_across_all_views(self):
        """Test search functionality across different views"""
        # Create test data
        credential = Credentials.objects.create(
            user=self.user,
            label="Searchable Gmail",
            type="email",
            username="search@gmail.com"
        )
        
        note = SecureNote.objects.create(
            user=self.user,
            title="Searchable Note",
            type="personal"
        )
        
        # Test search in credentials list
        cred_url = reverse('frontend:credentials_list')
        response = self.client.get(cred_url, {'query': 'Searchable'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Searchable Gmail')
        
        # Test search in notes list
        notes_url = reverse('frontend:notes_list')
        response = self.client.get(notes_url, {'query': 'Searchable'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Searchable Note')
        
        # Test global search page
        search_url = reverse('frontend:search')
        response = self.client.get(search_url, {'query': 'Searchable'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Searchable Gmail')
        self.assertContains(response, 'Searchable Note') 