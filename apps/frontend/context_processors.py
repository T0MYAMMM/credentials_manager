"""
Context processors for the frontend app
These functions provide global variables available in all templates.
"""

from apps.backend.models import Credentials, SecureNote
from apps.backend.business_logic import DashboardManager


def global_stats(request):
    """Provide global statistics for the sidebar/navigation"""
    if request.user.is_authenticated:
        try:
            stats = DashboardManager.get_dashboard_stats(request.user)
            return {
                'global_stats': {
                    'total_credentials': stats['total_credentials'],
                    'total_notes': stats['total_notes'],
                    'favorite_credentials': stats['favorite_credentials'],
                    'favorite_notes': stats['favorite_notes'],
                }
            }
        except Exception:
            # Return empty stats if there's an error
            return {
                'global_stats': {
                    'total_credentials': 0,
                    'total_notes': 0,
                    'favorite_credentials': 0,
                    'favorite_notes': 0,
                }
            }
    
    return {'global_stats': {}}


def app_info(request):
    """Provide app information for templates"""
    return {
        'app_name': 'Credentials Manager',
        'app_version': '2.0.0',
        'app_description': 'Secure password and note management system',
    }


def credential_types(request):
    """Provide credential types for forms and filters"""
    return {
        'credential_types': Credentials.CREDENTIAL_TYPES,
        'note_types': SecureNote.NOTE_TYPES,
    }
