from django.apps import AppConfig


class FrontendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.frontend'
    verbose_name = 'Frontend'
    
    def ready(self):
        """Initialize app when Django starts"""
        # Import any frontend-specific initialization here if needed
        pass 