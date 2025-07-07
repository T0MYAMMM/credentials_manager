from django.apps import AppConfig


class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.backend'
    verbose_name = 'Backend'
    
    def ready(self):
        """Initialize app when Django starts"""
        # Import signal handlers here if needed
        pass
