"""
Business Logic Module for Credentials Manager
This module contains all core business operations and utilities.
"""

from django.utils import timezone
from django.db.models import Q, Count
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
import csv

from .models import Credentials, SecureNote, ActivityLog
from .forms import CredentialForm, SecureNoteForm, SearchForm


class CredentialsManager:
    """Business logic for managing credentials"""
    
    @staticmethod
    def get_user_credentials(user, search_params=None):
        """Get filtered credentials for a user"""
        credentials = Credentials.objects.filter(user=user)
        
        if search_params:
            query = search_params.get('query')
            type_filter = search_params.get('type_filter')
            favorites_only = search_params.get('favorites_only')
            
            if query:
                credentials = credentials.filter(
                    Q(label__icontains=query) |
                    Q(username__icontains=query) |
                    Q(email__icontains=query) |
                    Q(note__icontains=query) |
                    Q(tags__icontains=query)
                )
            
            if type_filter and type_filter != 'all':
                credentials = credentials.filter(type=type_filter)
            
            if favorites_only:
                credentials = credentials.filter(is_favorite=True)
        
        return credentials
    
    @staticmethod
    def create_credential(user, form_data):
        """Create a new credential"""
        form = CredentialForm(form_data)
        if form.is_valid():
            credential = form.save(commit=False)
            credential.user = user
            credential.save()
            return credential, None
        return None, form.errors
    
    @staticmethod
    def update_credential(credential, form_data):
        """Update an existing credential"""
        form = CredentialForm(form_data, instance=credential)
        if form.is_valid():
            credential = form.save()
            return credential, None
        return None, form.errors
    
    @staticmethod
    def delete_credential(credential):
        """Delete a credential"""
        credential_label = credential.label
        credential.delete()
        return credential_label


class SecureNotesManager:
    """Business logic for managing secure notes"""
    
    @staticmethod
    def get_user_notes(user, search_params=None):
        """Get filtered notes for a user"""
        notes = SecureNote.objects.filter(user=user)
        
        if search_params:
            query = search_params.get('query')
            favorites_only = search_params.get('favorites_only')
            
            if query:
                notes = notes.filter(
                    Q(title__icontains=query) |
                    Q(tags__icontains=query)
                )
            
            if favorites_only:
                notes = notes.filter(is_favorite=True)
        
        return notes
    
    @staticmethod
    def create_note(user, form_data):
        """Create a new secure note"""
        form = SecureNoteForm(form_data)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = user
            note.save()
            return note, None
        return None, form.errors
    
    @staticmethod
    def update_note(note, form_data):
        """Update an existing note"""
        form = SecureNoteForm(form_data, instance=note)
        if form.is_valid():
            note = form.save()
            return note, None
        return None, form.errors
    
    @staticmethod
    def delete_note(note):
        """Delete a note"""
        note_title = note.title
        note.delete()
        return note_title


class DashboardManager:
    """Business logic for dashboard operations"""
    
    @staticmethod
    def get_dashboard_stats(user):
        """Get dashboard statistics for a user"""
        return {
            'total_credentials': Credentials.objects.filter(user=user).count(),
            'total_notes': SecureNote.objects.filter(user=user).count(),
            'favorite_credentials': Credentials.objects.filter(user=user, is_favorite=True).count(),
            'favorite_notes': SecureNote.objects.filter(user=user, is_favorite=True).count(),
            'recent_activities': ActivityLog.objects.filter(user=user)[:5],
            'recent_credentials': Credentials.objects.filter(user=user)[:5],
            'recent_notes': SecureNote.objects.filter(user=user)[:5],
            'credential_types': Credentials.objects.filter(user=user).values('type').annotate(
                count=Count('type')
            ).order_by('-count')[:5]
        }
    
    @staticmethod
    def get_recent_activities(user, limit=10):
        """Get recent activities for a user"""
        return ActivityLog.objects.filter(user=user)[:limit]


class ActivityManager:
    """Business logic for activity tracking"""
    
    @staticmethod
    def log_activity(user, action, description, request=None):
        """Log user activity"""
        activity = ActivityLog.objects.create(
            user=user,
            action=action,
            description=description,
            ip_address=request.META.get('REMOTE_ADDR') if request else None,
            user_agent=request.META.get('HTTP_USER_AGENT') if request else None,
        )
        return activity
    
    @staticmethod
    def get_user_activities(user, limit=50):
        """Get user activities"""
        return ActivityLog.objects.filter(user=user)[:limit]


class DataExportManager:
    """Business logic for data export operations"""
    
    @staticmethod
    def export_user_data(user):
        """Export user data as CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="credentials_export_{timezone.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        
        # Export credentials
        writer.writerow(['TYPE', 'LABEL', 'USERNAME', 'EMAIL', 'WEBSITE', 'NOTE', 'TAGS', 'CREATED'])
        
        for credential in Credentials.objects.filter(user=user):
            writer.writerow([
                credential.type,
                credential.label,
                credential.username or '',
                credential.email or '',
                credential.website_url or '',
                credential.note or '',
                credential.tags or '',
                credential.created_at.strftime('%Y-%m-%d')
            ])
        
        return response


class SearchManager:
    """Business logic for search operations"""
    
    @staticmethod
    def search_all_user_data(user, query=None, type_filter=None, favorites_only=False):
        """Search across all user data"""
        # Get credentials
        credentials = CredentialsManager.get_user_credentials(user, {
            'query': query,
            'type_filter': type_filter,
            'favorites_only': favorites_only
        })
        
        # Get notes
        notes = SecureNotesManager.get_user_notes(user, {
            'query': query,
            'favorites_only': favorites_only
        })
        
        return {
            'credentials': credentials,
            'notes': notes,
            'total_credentials': credentials.count(),
            'total_notes': notes.count(),
        }
    
    @staticmethod
    def get_search_form(get_data=None):
        """Get search form"""
        return SearchForm(get_data)


class PaginationManager:
    """Business logic for pagination"""
    
    @staticmethod
    def paginate_queryset(queryset, page_number, items_per_page=12):
        """Paginate a queryset"""
        paginator = Paginator(queryset, items_per_page)
        page_obj = paginator.get_page(page_number)
        return page_obj


class FavoriteManager:
    """Business logic for favorite operations"""
    
    @staticmethod
    def toggle_favorite(item, user):
        """Toggle favorite status for an item"""
        if hasattr(item, 'user') and item.user == user:
            item.is_favorite = not item.is_favorite
            item.save(update_fields=['is_favorite'])
            return item.is_favorite
        return False
    
    @staticmethod
    def get_user_favorites(user):
        """Get all favorite items for a user"""
        return {
            'credentials': Credentials.objects.filter(user=user, is_favorite=True),
            'notes': SecureNote.objects.filter(user=user, is_favorite=True),
        }


class AccessTracker:
    """Business logic for tracking item access"""
    
    @staticmethod
    def update_access_time(item, user):
        """Update last accessed time for an item"""
        if hasattr(item, 'user') and item.user == user:
            item.last_accessed = timezone.now()
            item.save(update_fields=['last_accessed'])
            return True
        return False
