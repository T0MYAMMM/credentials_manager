from django.apps import AppConfig


class FrontendConfig(AppConfig):
    label = 'apps_frontend'
    name = 'apps.frontend'
    verbose_name = 'Frontend'
    
    def ready(self):
        """Initialize app when Django starts"""
        # Import any frontend-specific initialization here if needed
        pass 