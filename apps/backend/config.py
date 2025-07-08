from django.apps import AppConfig


class BackendConfig(AppConfig):
    label = 'apps_backend'
    name = 'apps.backend'
    verbose_name = 'Backend'
    
    def ready(self):
        """Initialize app when Django starts"""
        # Import signal handlers here if needed
        pass
