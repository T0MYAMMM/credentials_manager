"""
ASGI config for credentials_manager project.

This module contains the ASGI application used by Django's development server
and any production ASGI deployments. It should expose a module-level variable
named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

# If you're using channels or other ASGI frameworks, you can combine them here
# For example:
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import your_app.routing

application = django_asgi_app

# Alternative configuration for channels (if using WebSockets)
# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             # Add your WebSocket URL patterns here
#         ])
#     ),
# })
