"""
URL configuration for credentials_manager project.

This configuration provides:
- Main application routing
- API versioning support
- Development tools integration
- Error handling pages
- Static/media file serving for development
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse

def health_check(request):
    """Simple health check endpoint for monitoring"""
    return HttpResponse(b"OK", content_type="text/plain")

def robots_txt(request):
    """Robots.txt file for web crawlers"""
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /api/",
        "Disallow: /auth/",
        "Disallow: /media/private/",
    ]
    return HttpResponse("\n".join(lines).encode('utf-8'), content_type="text/plain")

# Core URL patterns
urlpatterns = [
    # Admin interface
    path(settings.ADMIN_URL, admin.site.urls),
    
    # Authentication
    path('auth/', include('apps.authentication.urls')),
    
    # API endpoints
    path('api/', include('apps.backend.urls')),
    
    # Frontend application
    path('dashboard/', include('apps.frontend.urls')),
    
    # Utility endpoints
    path('health/', health_check, name='health_check'),
    path('robots.txt', robots_txt, name='robots_txt'),
    
    # Root redirect (if someone accesses just the domain)
    path('', lambda request: redirect('frontend:dashboard'), name='root_redirect'),
]

# Custom error handlers (disabled - using Django defaults)
# handler400 = 'core.views.bad_request'
# handler403 = 'core.views.permission_denied'
# handler404 = 'core.views.page_not_found'
# handler500 = 'core.views.server_error'

# Development-specific URLs
if settings.DEBUG:
    # Static and media files serving
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Django Debug Toolbar (if installed)
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
    
    # Development API documentation (if needed)
    urlpatterns += [
        path('api-docs/', TemplateView.as_view(
            template_name='api_docs.html',
            extra_context={'title': 'API Documentation'}
        ), name='api_docs'),
    ]

# Future API versioning can be added here if needed
# Example:
# if hasattr(settings, 'API_VERSIONING') and settings.API_VERSIONING:
#     urlpatterns += [
#         path('api/v1/', include('apps.backend.urls')),
#         path('api/v2/', include('apps.backend_v2.urls')),
#     ]

# Admin site customization
admin.site.site_header = "Credentials Manager Administration"
admin.site.site_title = "Credentials Manager Admin"
admin.site.index_title = "Welcome to Credentials Manager Administration"

# Additional security headers (can be moved to middleware if needed)
if not settings.DEBUG:
    # Add additional production-specific URL patterns
    urlpatterns += [
        # Security.txt for security researchers
        path('.well-known/security.txt', TemplateView.as_view(
            template_name='security.txt',
            content_type='text/plain'
        ), name='security_txt'),
    ]
