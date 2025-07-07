"""
WSGI config for credentials_manager project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Get the Django WSGI application
application = get_wsgi_application()

# Production optimizations can be added here if needed
# For example, if using whitenoise for static files:
# from whitenoise import WhiteNoise
# application = WhiteNoise(application, root='/path/to/static/files')
