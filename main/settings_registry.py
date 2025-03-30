"""
Settings Registry - Manages loading and accessing settings from the database
with proper caching to minimize database queries
"""
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Cache timeout for settings - default 1 hour
SETTINGS_CACHE_TIMEOUT = getattr(settings, 'SETTINGS_CACHE_TIMEOUT', 3600)
SETTINGS_CACHE_KEY = 'site_settings_registry'

class SettingsRegistry:
    """
    Settings registry that handles loading settings from the database
    and provides cached access to them
    """
    _instance = None
    _initialized = False
    _settings_cache = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsRegistry, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Don't automatically load settings on initialization
        # This avoids database access during Django startup
        pass
    
    def is_ready(self):
        """Check if the registry has been initialized"""
        return SettingsRegistry._initialized
    
    def _ensure_initialized(self):
        """Ensure settings are loaded when needed, not at import time"""
        if not SettingsRegistry._initialized:
            self.reload_settings()
            SettingsRegistry._initialized = True
    
    def reload_settings(self):
        """Reload settings from the database and update cache"""
        from main.models import SiteSettings
        
        try:
            # Get settings from cache first
            cached_settings = cache.get(SETTINGS_CACHE_KEY)
            if cached_settings:
                self._settings_cache = cached_settings
                logger.debug("Settings loaded from cache")
                SettingsRegistry._initialized = True
                return
                
            # If not in cache, load from DB
            site_settings = SiteSettings.get_settings()
            
            # Convert model instance to dictionary
            settings_dict = {}
            
            # Basic site info
            settings_dict['SITE_NAME'] = site_settings.site_name
            settings_dict['SITE_TAGLINE'] = site_settings.site_tagline
            settings_dict['COMPANY_ADDRESS'] = site_settings.address
            settings_dict['COMPANY_PHONE'] = site_settings.phone
            settings_dict['COMPANY_EMAIL'] = site_settings.email
            
            # About us content
            settings_dict['ABOUT_US_SHORT'] = site_settings.about_us_short
            settings_dict['ABOUT_US_FULL'] = site_settings.about_us_full
            
            # Social media links
            settings_dict['FACEBOOK_URL'] = site_settings.facebook_url
            settings_dict['TWITTER_URL'] = site_settings.twitter_url
            settings_dict['INSTAGRAM_URL'] = site_settings.instagram_url
            settings_dict['LINKEDIN_URL'] = site_settings.linkedin_url
            settings_dict['YOUTUBE_URL'] = site_settings.youtube_url
            
            # SEO Settings
            settings_dict['META_DESCRIPTION'] = site_settings.meta_description
            settings_dict['META_KEYWORDS'] = site_settings.meta_keywords
            
            # Google Analytics
            settings_dict['GOOGLE_ANALYTICS_ID'] = site_settings.google_analytics_id
            
            # Company info
            settings_dict['ESTABLISHED_YEAR'] = site_settings.established_year
            
            # Footer content
            settings_dict['FOOTER_TEXT'] = site_settings.footer_text
            
            # Cache settings
            settings_dict['CACHE_TIMEOUT'] = site_settings.cache_timeout
            
            # Get logo and favicon URLs if they exist
            if site_settings.company_logo:
                settings_dict['COMPANY_LOGO_URL'] = site_settings.company_logo.url
            
            if site_settings.favicon:
                settings_dict['FAVICON_URL'] = site_settings.favicon.url
            
            # Update instance cache
            self._settings_cache = settings_dict
            
            # Set in Django cache
            cache.set(SETTINGS_CACHE_KEY, settings_dict, SETTINGS_CACHE_TIMEOUT)
            
            logger.debug("Settings loaded from database and cached")
            SettingsRegistry._initialized = True
            
        except Exception as e:
            logger.error(f"Error loading settings from database: {str(e)}")
            # If there's an error, use an empty dict but don't cache it
            self._settings_cache = {}
    
    def get(self, key, default=None):
        """Get a setting value by key with optional default"""
        self._ensure_initialized()
        return self._settings_cache.get(key, default)
    
    def get_all(self):
        """Get all settings as a dictionary"""
        self._ensure_initialized()
        return self._settings_cache.copy()
    
    def clear_cache(self):
        """Clear the settings cache"""
        cache.delete(SETTINGS_CACHE_KEY)
        self._settings_cache = {}
        SettingsRegistry._initialized = False
        logger.debug("Settings cache cleared")

# Singleton instance - just create the instance but don't load settings yet
settings_registry = SettingsRegistry()

def get_setting(key, default=None):
    """Convenience function to get a setting value"""
    return settings_registry.get(key, default)

def reload_settings():
    """Convenience function to reload settings"""
    settings_registry.reload_settings()

def clear_settings_cache():
    """Convenience function to clear settings cache"""
    settings_registry.clear_cache() 