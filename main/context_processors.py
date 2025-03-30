from django.core.cache import cache
from .models import SiteSettings
from .settings_registry import settings_registry
import logging

logger = logging.getLogger(__name__)

def site_settings(request):
    """
    Context processor that adds site settings to all templates
    """
    try:
        # Get settings model instance for backward compatibility
        settings_model = SiteSettings.get_settings()
        
        # Get settings from registry for new approach
        registry_settings = settings_registry.get_all()
        
        # Return context dict with both the model instance and registry settings
        return {
            'site_settings': settings_model,
            'settings': registry_settings
        }
    except Exception as e:
        # Log the error and return empty dict
        logger.error(f"Error in site_settings context processor: {str(e)}")
        return {} 