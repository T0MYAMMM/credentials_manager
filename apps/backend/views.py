"""
Backend API Views and Business Logic
This module contains API endpoints and business logic functions that can be used by the frontend.
"""

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q, Count
import json

from .models import Credentials, SecureNote, ActivityLog
from .forms import CredentialForm, SecureNoteForm, SearchForm


# API Endpoints for AJAX requests
@login_required
@require_POST
def api_toggle_favorite(request):
    """API endpoint to toggle favorite status"""
    try:
        data = json.loads(request.body)
        item_type = data.get('type')
        item_id = data.get('id')
        
        if item_type == 'credential':
            item = Credentials.objects.get(pk=item_id, user=request.user)
        elif item_type == 'note':
            item = SecureNote.objects.get(pk=item_id, user=request.user)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid type'})
        
        item.is_favorite = not item.is_favorite
        item.save(update_fields=['is_favorite'])
        
        return JsonResponse({
            'success': True,
            'is_favorite': item.is_favorite
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_GET
def api_user_stats(request):
    """API endpoint to get user statistics"""
    user = request.user
    
    stats = {
        'total_credentials': Credentials.objects.filter(user=user).count(),
        'total_notes': SecureNote.objects.filter(user=user).count(),
        'favorite_credentials': Credentials.objects.filter(user=user, is_favorite=True).count(),
        'favorite_notes': SecureNote.objects.filter(user=user, is_favorite=True).count(),
        'recent_activities': list(ActivityLog.objects.filter(user=user)[:5].values(
            'action', 'description', 'timestamp'
        )),
        'credential_types': list(Credentials.objects.filter(user=user).values('type').annotate(
            count=Count('type')
        ).order_by('-count')[:5])
    }
    
    return JsonResponse(stats)


@login_required
@require_POST
def api_search(request):
    """API endpoint for searching credentials and notes"""
    try:
        data = json.loads(request.body)
        query = data.get('query', '')
        type_filter = data.get('type_filter', 'all')
        favorites_only = data.get('favorites_only', False)
        
        # Search credentials
        credentials = Credentials.objects.filter(user=request.user)
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
        
        # Search notes
        notes = SecureNote.objects.filter(user=request.user)
        if query:
            notes = notes.filter(
                Q(title__icontains=query) |
                Q(tags__icontains=query)
            )
        if favorites_only:
            notes = notes.filter(is_favorite=True)
        
        return JsonResponse({
            'credentials': list(credentials.values('id', 'label', 'type', 'username', 'email', 'is_favorite', 'updated_at')),
            'notes': list(notes.values('id', 'title', 'type', 'is_favorite', 'updated_at')),
            'total_credentials': credentials.count(),
            'total_notes': notes.count(),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# Business Logic Functions (can be imported by frontend)
def get_user_dashboard_data(user):
    """Get dashboard data for a user"""
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


def search_user_data(user, query=None, type_filter=None, favorites_only=False):
    """Search user credentials and notes"""
    # Search credentials
    credentials = Credentials.objects.filter(user=user)
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
    
    # Search notes
    notes = SecureNote.objects.filter(user=user)
    if query:
        notes = notes.filter(
            Q(title__icontains=query) |
            Q(tags__icontains=query)
        )
    if favorites_only:
        notes = notes.filter(is_favorite=True)
    
    return {
        'credentials': credentials,
        'notes': notes,
        'total_credentials': credentials.count(),
        'total_notes': notes.count(),
    }


def update_item_access_time(item, user):
    """Update the last accessed time for an item"""
    if hasattr(item, 'user') and item.user == user:
        item.last_accessed = timezone.now()
        item.save(update_fields=['last_accessed'])


def log_user_activity(user, action, description, request=None):
    """Log user activity for security tracking"""
    activity = ActivityLog.objects.create(
        user=user,
        action=action,
        description=description,
        ip_address=request.META.get('REMOTE_ADDR') if request else None,
        user_agent=request.META.get('HTTP_USER_AGENT') if request else None,
    )
    return activity
