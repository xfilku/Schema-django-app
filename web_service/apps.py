"""
App configuration for the 'web_service' Django application.

This class defines metadata and startup behavior for the app.
"""

from django.apps import AppConfig

class WebServiceConfig(AppConfig):
    """
    Configuration class for the web_service app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_service'

    def ready(self):
        """
        Executes application-specific startup logic.

        Used here to import signal handlers when the app is ready.
        This ensures signals are connected once the app is initialized.
        """
        import web_service.signals  # noqa: F401 - side-effect import
