"""
Core views for error handling and utility functions
"""

from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError
from django.template import RequestContext
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def bad_request(request, exception=None):
    """
    Custom 400 Bad Request error handler
    """
    logger.warning(f"400 Bad Request: {request.path} from {request.META.get('REMOTE_ADDR')}")
    
    context = {
        'error_code': 400,
        'error_title': 'Bad Request',
        'error_message': 'The request could not be understood by the server.',
        'show_details': settings.DEBUG,
        'exception': str(exception) if exception and settings.DEBUG else None
    }
    
    return render(request, 'errors/400.html', context, status=400)

def permission_denied(request, exception=None):
    """
    Custom 403 Permission Denied error handler
    """
    logger.warning(f"403 Permission Denied: {request.path} from {request.META.get('REMOTE_ADDR')}")
    
    context = {
        'error_code': 403,
        'error_title': 'Permission Denied',
        'error_message': 'You do not have permission to access this resource.',
        'show_details': settings.DEBUG,
        'exception': str(exception) if exception and settings.DEBUG else None
    }
    
    return render(request, 'errors/403.html', context, status=403)

def page_not_found(request, exception=None):
    """
    Custom 404 Page Not Found error handler
    """
    logger.info(f"404 Not Found: {request.path} from {request.META.get('REMOTE_ADDR')}")
    
    context = {
        'error_code': 404,
        'error_title': 'Page Not Found',
        'error_message': 'The requested page could not be found.',
        'show_details': settings.DEBUG,
        'exception': str(exception) if exception and settings.DEBUG else None,
        'request_path': request.path
    }
    
    return render(request, 'errors/404.html', context, status=404)

def server_error(request):
    """
    Custom 500 Internal Server Error handler
    """
    logger.error(f"500 Internal Server Error: {request.path} from {request.META.get('REMOTE_ADDR')}")
    
    context = {
        'error_code': 500,
        'error_title': 'Internal Server Error',
        'error_message': 'An unexpected error occurred while processing your request.',
        'show_details': settings.DEBUG
    }
    
    return render(request, 'errors/500.html', context, status=500) 