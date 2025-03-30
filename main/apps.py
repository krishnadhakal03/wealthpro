from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    
    def ready(self):
        """
        Initialize application when Django starts.
        This is the place to perform startup operations.
        """
        # Initialize settings registry
        try:
            # Import here to avoid circular imports
            from .settings_registry import settings_registry
            
            # Force load settings
            settings_registry.reload_settings()
            logger.info("Settings registry initialized")
        except Exception as e:
            logger.error(f"Error initializing settings registry: {str(e)}")
        
        # Other startup operations can go here
        pass
