"""
REST API endpoints for the backend
This module provides RESTful API endpoints that can be used by the frontend or external applications.
"""

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import get_object_or_404
import json

from .models import Credentials, SecureNote, ActivityLog
from .business_logic import (
    CredentialsManager, SecureNotesManager, DashboardManager,
    ActivityManager, SearchManager, FavoriteManager, AccessTracker
)


class APIView(View):
    """Base API view with common functionality"""
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_json_data(self, request):
        """Parse JSON data from request"""
        try:
            return json.loads(request.body)
        except json.JSONDecodeError:
            return None
    
    def json_response(self, data, status=200):
        """Return JSON response"""
        return JsonResponse(data, status=status)
    
    def error_response(self, error_message, status=400):
        """Return error response"""
        return JsonResponse({'error': error_message}, status=status)


class DashboardStatsAPI(APIView):
    """API endpoint for dashboard statistics"""
    
    def get(self, request):
        """Get dashboard statistics"""
        try:
            stats = DashboardManager.get_dashboard_stats(request.user)
            
            # Convert querysets to lists for JSON serialization
            stats['recent_activities'] = list(stats['recent_activities'].values(
                'action', 'description', 'timestamp'
            ))
            stats['recent_credentials'] = list(stats['recent_credentials'].values(
                'id', 'label', 'type', 'username', 'updated_at'
            ))
            stats['recent_notes'] = list(stats['recent_notes'].values(
                'id', 'title', 'type', 'updated_at'
            ))
            
            return self.json_response(stats)
        except Exception as e:
            return self.error_response(str(e))


class SearchAPI(APIView):
    """API endpoint for searching data"""
    
    def post(self, request):
        """Search credentials and notes"""
        try:
            data = self.get_json_data(request)
            if not data:
                return self.error_response('Invalid JSON data')
            
            query = data.get('query', '')
            type_filter = data.get('type_filter', 'all')
            favorites_only = data.get('favorites_only', False)
            
            results = SearchManager.search_all_user_data(
                request.user, query, type_filter, favorites_only
            )
            
            # Convert querysets to lists for JSON serialization
            results['credentials'] = list(results['credentials'].values(
                'id', 'label', 'type', 'username', 'email', 'is_favorite', 'updated_at'
            ))
            results['notes'] = list(results['notes'].values(
                'id', 'title', 'type', 'is_favorite', 'updated_at'
            ))
            
            return self.json_response(results)
        except Exception as e:
            return self.error_response(str(e))


class FavoriteToggleAPI(APIView):
    """API endpoint for toggling favorites"""
    
    def post(self, request):
        """Toggle favorite status"""
        try:
            data = self.get_json_data(request)
            if not data:
                return self.error_response('Invalid JSON data')
            
            item_type = data.get('type')
            item_id = data.get('id')
            
            if item_type == 'credential':
                item = get_object_or_404(Credentials, pk=item_id, user=request.user)
            elif item_type == 'note':
                item = get_object_or_404(SecureNote, pk=item_id, user=request.user)
            else:
                return self.error_response('Invalid item type')
            
            is_favorite = FavoriteManager.toggle_favorite(item, request.user)
            
            return self.json_response({
                'success': True,
                'is_favorite': is_favorite
            })
        except Exception as e:
            return self.error_response(str(e))


class CredentialsAPI(APIView):
    """API endpoint for credentials management"""
    
    def get(self, request):
        """Get user credentials"""
        try:
            search_params = {
                'query': request.GET.get('query'),
                'type_filter': request.GET.get('type_filter'),
                'favorites_only': request.GET.get('favorites_only') == 'true'
            }
            
            credentials = CredentialsManager.get_user_credentials(request.user, search_params)
            
            return self.json_response({
                'credentials': list(credentials.values()),
                'total': credentials.count()
            })
        except Exception as e:
            return self.error_response(str(e))
    
    def post(self, request):
        """Create a new credential"""
        try:
            data = self.get_json_data(request)
            if not data:
                return self.error_response('Invalid JSON data')
            
            credential, errors = CredentialsManager.create_credential(request.user, data)
            
            if credential:
                # Log activity
                ActivityManager.log_activity(
                    request.user, 'create_credential', 
                    f'Created credential: {credential.label}', request
                )
                
                return self.json_response({
                    'success': True,
                    'credential': {
                        'id': credential.id,
                        'label': credential.label,
                        'type': credential.type
                    }
                })
            else:
                return self.error_response(errors)
        except Exception as e:
            return self.error_response(str(e))


class NotesAPI(APIView):
    """API endpoint for notes management"""
    
    def get(self, request):
        """Get user notes"""
        try:
            search_params = {
                'query': request.GET.get('query'),
                'favorites_only': request.GET.get('favorites_only') == 'true'
            }
            
            notes = SecureNotesManager.get_user_notes(request.user, search_params)
            
            return self.json_response({
                'notes': list(notes.values()),
                'total': notes.count()
            })
        except Exception as e:
            return self.error_response(str(e))
    
    def post(self, request):
        """Create a new note"""
        try:
            data = self.get_json_data(request)
            if not data:
                return self.error_response('Invalid JSON data')
            
            note, errors = SecureNotesManager.create_note(request.user, data)
            
            if note:
                # Log activity
                ActivityManager.log_activity(
                    request.user, 'create_note', 
                    f'Created note: {note.title}', request
                )
                
                return self.json_response({
                    'success': True,
                    'note': {
                        'id': note.id,
                        'title': note.title,
                        'type': note.type
                    }
                })
            else:
                return self.error_response(errors)
        except Exception as e:
            return self.error_response(str(e))


class ActivityLogAPI(APIView):
    """API endpoint for activity logs"""
    
    def get(self, request):
        """Get user activity logs"""
        try:
            limit = int(request.GET.get('limit', 50))
            activities = ActivityManager.get_user_activities(request.user, limit)
            
            return self.json_response({
                'activities': list(activities.values(
                    'action', 'description', 'timestamp', 'ip_address'
                )),
                'total': activities.count()
            })
        except Exception as e:
            return self.error_response(str(e))


# Function-based API views (for backward compatibility)
@login_required
@require_GET
def api_user_stats(request):
    """Get user statistics (function-based view)"""
    view = DashboardStatsAPI()
    return view.get(request)


@login_required
@require_POST
def api_search(request):
    """Search data (function-based view)"""
    view = SearchAPI()
    return view.post(request)


@login_required
@require_POST
def api_toggle_favorite(request):
    """Toggle favorite (function-based view)"""
    view = FavoriteToggleAPI()
    return view.post(request)
