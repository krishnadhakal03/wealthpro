"""
Settings Service - Helper functions for interacting with app settings.
This module provides convenience functions for views and business logic
to interact with the settings registry.
"""
import os
from django.conf import settings as django_settings
from .settings_registry import get_setting, reload_settings, clear_settings_cache, settings_registry
import logging

logger = logging.getLogger(__name__)

PRESET_THEME_PALETTES = {
    'default_blue': {'primary': '#0D6EFD', 'accent': '#38BDF8'},
    'premium_dark': {'primary': '#02070F', 'accent': '#3B82F6'},
    'trust_navy': {'primary': '#0B1F3A', 'accent': '#2F80ED'},
    'modern_teal': {'primary': '#0F3D3E', 'accent': '#2DD4BF'},
    'executive_gold': {'primary': '#111827', 'accent': '#D4AF37'},
    'custom': {'primary': '#02070F', 'accent': '#3B82F6'},
}

DEFAULT_THEME = {
    'primary': '#02070F',
    'primary_hover': '#0B1220',
    'accent': '#3B82F6',
    'accent_hover': '#2563EB',
    'button_bg': '#02070F',
    'button_text': '#FFFFFF',
    'navbar_bg': '#02070F',
    'navbar_text': '#FFFFFF',
    'navbar_link_hover': '#60A5FA',
    'footer_bg': '#02070F',
    'footer_text': '#CBD5E1',
    'link_color': '#2563EB',
    'heading_color': '#111827',
    'body_text': '#374151',
    'page_bg': '#F8FAFC',
    'card_bg': '#FFFFFF',
    'border_color': '#E5E7EB',
}


def _hex_to_rgb(color):
    value = color.strip().lstrip('#')
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


def _rgb_to_hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(*[max(0, min(255, int(channel))) for channel in rgb])


def _mix(color, target, weight):
    rgb = _hex_to_rgb(color)
    target_rgb = _hex_to_rgb(target)
    return _rgb_to_hex(
        rgb[index] + (target_rgb[index] - rgb[index]) * weight
        for index in range(3)
    )


def _relative_luminance(color):
    rgb = [channel / 255 for channel in _hex_to_rgb(color)]
    linear = [
        channel / 12.92 if channel <= 0.03928 else ((channel + 0.055) / 1.055) ** 2.4
        for channel in rgb
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _readable_text_for(color):
    return '#FFFFFF' if _relative_luminance(color) < 0.45 else '#111827'


def _hover_for(color):
    return _mix(color, '#FFFFFF', 0.12) if _relative_luminance(color) < 0.45 else _mix(color, '#000000', 0.12)


def get_theme_settings():
    """
    Get admin-managed theme settings as CSS-ready palette values.
    """
    theme_mode = get_setting('THEME_MODE', 'premium_dark')
    preset = PRESET_THEME_PALETTES.get(theme_mode, PRESET_THEME_PALETTES['premium_dark'])
    primary = get_setting('THEME_PRIMARY_COLOR', preset['primary']) or preset['primary']
    accent = get_setting('THEME_ACCENT_COLOR', preset['accent']) or preset['accent']
    use_smart_palette = get_setting('THEME_USE_SMART_PALETTE', True)

    if use_smart_palette and theme_mode == 'premium_dark' and primary.upper() == '#02070F':
        return DEFAULT_THEME.copy()

    button_text = _readable_text_for(primary)
    footer_text = '#CBD5E1' if _relative_luminance(primary) < 0.45 else '#374151'

    return {
        'primary': primary,
        'primary_hover': _hover_for(primary),
        'accent': accent,
        'accent_hover': _hover_for(accent),
        'button_bg': primary,
        'button_text': button_text,
        'navbar_bg': primary,
        'navbar_text': button_text,
        'navbar_link_hover': _mix(accent, '#FFFFFF', 0.25) if _relative_luminance(primary) < 0.45 else _hover_for(accent),
        'footer_bg': primary,
        'footer_text': footer_text,
        'link_color': accent,
        'heading_color': '#111827',
        'body_text': '#374151',
        'page_bg': '#F8FAFC',
        'card_bg': '#FFFFFF',
        'border_color': '#E5E7EB',
    }

def get_email_settings():
    """
    Get email settings from the SiteSettings model or fallback to Django settings.
    
    Returns a dictionary with all email-related settings.
    """
    # Initialize with values from Django settings
    email_settings = {
        'EMAIL_HOST': getattr(django_settings, 'EMAIL_HOST', ''),
        'EMAIL_PORT': getattr(django_settings, 'EMAIL_PORT', 587),
        'EMAIL_USE_TLS': getattr(django_settings, 'EMAIL_USE_TLS', True),
        'EMAIL_USE_SSL': getattr(django_settings, 'EMAIL_USE_SSL', False),
        'EMAIL_HOST_USER': getattr(django_settings, 'EMAIL_HOST_USER', ''),
        'EMAIL_HOST_PASSWORD': getattr(django_settings, 'EMAIL_HOST_PASSWORD', ''),
        'DEFAULT_FROM_EMAIL': getattr(django_settings, 'DEFAULT_FROM_EMAIL', ''),
        'CONTACT_EMAIL': getattr(django_settings, 'CONTACT_EMAIL', ''),
        'EMAIL_PROVIDER': 'smtp',
        'AWS_REGION': 'us-east-1',
    }
    
    # Override with values from database if available
    if settings_registry.is_ready():
        db_settings = settings_registry.get_all()
        if db_settings:
            email_settings.update({
                'EMAIL_HOST': db_settings.get('EMAIL_HOST', email_settings['EMAIL_HOST']),
                'EMAIL_PORT': db_settings.get('EMAIL_PORT', email_settings['EMAIL_PORT']),
                'EMAIL_USE_TLS': db_settings.get('EMAIL_USE_TLS', email_settings['EMAIL_USE_TLS']),
                'EMAIL_USE_SSL': db_settings.get('EMAIL_USE_SSL', email_settings['EMAIL_USE_SSL']),
                'EMAIL_HOST_USER': db_settings.get('EMAIL_HOST_USER', email_settings['EMAIL_HOST_USER']),
                'EMAIL_HOST_PASSWORD': db_settings.get('EMAIL_HOST_PASSWORD', email_settings['EMAIL_HOST_PASSWORD']),
                'DEFAULT_FROM_EMAIL': db_settings.get('DEFAULT_FROM_EMAIL', email_settings['DEFAULT_FROM_EMAIL']),
                'CONTACT_EMAIL': db_settings.get('CONTACT_EMAIL', email_settings['CONTACT_EMAIL']),
                'EMAIL_PROVIDER': db_settings.get('EMAIL_PROVIDER', email_settings['EMAIL_PROVIDER']),
                'AWS_REGION': db_settings.get('AWS_REGION', email_settings['AWS_REGION']),
            })
    
    return email_settings

def get_security_settings():
    """
    Get security settings from the SiteSettings model or fallback to Django settings.
    
    Returns a dictionary with all security-related settings.
    """
    # Initialize with values from Django settings
    security_settings = {
        'CSRF_PROTECTION': getattr(django_settings, 'CSRF_COOKIE_SECURE', True),
        'SECURE_COOKIES': getattr(django_settings, 'SESSION_COOKIE_SECURE', True),
        'SSL_REDIRECT': getattr(django_settings, 'SECURE_SSL_REDIRECT', True),
    }
    
    # Override with values from database if available
    if settings_registry.is_ready():
        db_settings = settings_registry.get_all()
        if db_settings:
            security_settings.update({
                'CSRF_PROTECTION': db_settings.get('ENABLE_CSRF_PROTECTION', security_settings['CSRF_PROTECTION']),
                'SECURE_COOKIES': db_settings.get('ENABLE_SECURE_COOKIES', security_settings['SECURE_COOKIES']),
                'SSL_REDIRECT': db_settings.get('ENABLE_SSL_REDIRECT', security_settings['SSL_REDIRECT']),
            })
    
    return security_settings

def get_site_info():
    """
    Get basic site information settings
    Returns a dictionary with site settings
    """
    site_info = {
        'SITE_NAME': get_setting('SITE_NAME', 'Next Generation Wealth Pro'),
        'SITE_TAGLINE': get_setting('SITE_TAGLINE', 'Wealth Management'),
        'COMPANY_ADDRESS': get_setting('COMPANY_ADDRESS', '123 Street, New York, USA'),
        'COMPANY_PHONE': get_setting('COMPANY_PHONE', '+012 345 67890'),
        'COMPANY_EMAIL': get_setting('COMPANY_EMAIL', 'info@nextgenwealthpro.com'),
        'ABOUT_US_SHORT': get_setting('ABOUT_US_SHORT', 'Next Generation Wealth Pro provides comprehensive wealth management services.'),
        'ABOUT_US_FULL': get_setting('ABOUT_US_FULL', ''),
        'ESTABLISHED_YEAR': get_setting('ESTABLISHED_YEAR', None),
        'FOOTER_TEXT': get_setting('FOOTER_TEXT', '')
    }
    return site_info

def get_social_media_urls():
    """
    Get social media URLs from the SiteSettings model.
    
    Returns a dictionary with all social media URLs.
    """
    social_media = {
        'FACEBOOK_URL': '',
        'TWITTER_URL': '',
        'INSTAGRAM_URL': '',
        'LINKEDIN_URL': '',
        'YOUTUBE_URL': '',
    }
    
    # Get values from database if available
    if settings_registry.is_ready():
        db_settings = settings_registry.get_all()
        if db_settings:
            social_media.update({
                'FACEBOOK_URL': db_settings.get('FACEBOOK_URL', ''),
                'TWITTER_URL': db_settings.get('TWITTER_URL', ''),
                'INSTAGRAM_URL': db_settings.get('INSTAGRAM_URL', ''),
                'LINKEDIN_URL': db_settings.get('LINKEDIN_URL', ''),
                'YOUTUBE_URL': db_settings.get('YOUTUBE_URL', ''),
            })
    
    return social_media

def get_maps_settings():
    """
    Get Google Maps settings
    Returns the Google Maps embed URL
    """
    default_map_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3022.9663095343016!2d-74.00425882426698!3d40.71116937132799!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c25a23e28c1191%3A0x49f75d3281df052a!2s150%20Park%20Row%2C%20New%20York%2C%20NY%2010007%2C%20USA!5e0!3m2!1sen!2sbg!4v1685637930992!5m2!1sen!2sbg"
    return get_setting('GOOGLE_MAPS_EMBED_URL', default_map_url)

def get_business_hours():
    """
    Get the business hours settings from registry.
    Returns a dictionary with days of week and their hours.
    """
    # Default business hours
    business_hours = {
        'WEEKDAYS': '9:00 AM - 5:00 PM',
        'SATURDAY': 'By appointment',
        'SUNDAY': 'Closed',
    }
    
    # Override with values from database if available
    if settings_registry.is_ready():
        db_settings = settings_registry.get_all()
        if db_settings:
            business_hours.update({
                'WEEKDAYS': db_settings.get('BUSINESS_HOURS_WEEKDAYS', business_hours['WEEKDAYS']),
                'SATURDAY': db_settings.get('BUSINESS_HOURS_SATURDAY', business_hours['SATURDAY']),
                'SUNDAY': db_settings.get('BUSINESS_HOURS_SUNDAY', business_hours['SUNDAY']),
            })
    
    return business_hours 
