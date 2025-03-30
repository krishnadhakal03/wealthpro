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
        # Import settings registry but don't force loading
        try:
            # Import here to avoid circular imports
            from .settings_registry import settings_registry
            
            # Log that the registry is imported but not loaded
            logger.info("Settings registry initialized - will load on first access")
        except Exception as e:
            logger.error(f"Error importing settings registry: {str(e)}")
        
        # Other startup operations can go here
        pass
