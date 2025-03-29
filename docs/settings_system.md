# WealthPro Database-Driven Settings System

## Overview

The WealthPro application uses a database-driven settings system that allows configuration of various aspects of the site without modifying code. This document explains how the system works and how to use it.

## Core Components

### 1. `SiteSettings` Model

This Django model stores all configurable settings and provides default values. It includes:

- Basic site information (name, tagline)
- Contact details (address, phone, email)
- Social media links
- Email configuration
- Business hours
- Security settings
- Google Maps configuration

The model is designed as a singleton, meaning only one instance can exist in the database.

### 2. Settings Registry

The `SettingsRegistry` class (`main/settings_registry.py`) manages loading settings from the database and provides cached access to them:

- Loads settings from the database on application startup
- Caches settings to avoid repeated database queries
- Provides a simple API for accessing settings

### 3. Settings Service

The `settings_service.py` module provides helper functions for accessing specific groups of settings:

- Email settings (`get_email_settings()`)
- Security settings (`get_security_settings()`)
- Site info (`get_site_info()`)
- Social media URLs (`get_social_media_urls()`)
- Maps settings (`get_maps_settings()`)
- Business hours (`get_business_hours()`)

### 4. Context Processor

The context processor adds settings to all templates:
- `site_settings`: Direct access to the SiteSettings model instance
- `settings`: Dictionary of all settings from the registry

## How to Use

### In Templates

Settings can be accessed directly in templates using either `site_settings` or `settings`:

```html
<!-- Using the model instance (legacy approach) -->
<h1>{{ site_settings.site_name }}</h1>

<!-- Using the settings registry (new approach) -->
<h1>{{ settings.SITE_NAME }}</h1>
```

### In Views

For views, use the settings service:

```python
from main.settings_service import get_email_settings, get_site_info

def some_view(request):
    # Get email settings
    email_settings = get_email_settings()
    contact_email = email_settings['CONTACT_EMAIL']
    
    # Get site info
    site_info = get_site_info()
    site_name = site_info['SITE_NAME']
    
    # Use the settings
    # ...
```

### In Admin

The admin interface provides a user-friendly way to manage settings:

1. Go to the admin panel at `/admin/`
2. Navigate to the "Site Settings" section
3. Update settings as needed

When you save changes in the admin, the settings cache is automatically refreshed.

## Deployment Considerations

### Production Settings

In production, you have two options:

1. **Use settings.py for critical settings**:
   - Database credentials
   - Secret keys
   - Debug flags
   - Allowed hosts

2. **Use database for everything else**:
   - Site name, contact info, etc.
   - Email configuration
   - Security settings

### Initial Setup

On a fresh deployment:

1. Run migrations to create the SiteSettings model
2. Access the admin panel and configure settings
3. Restart the application to ensure all settings are loaded

### Cache Considerations

Settings are cached to improve performance. If you update settings directly in the database (outside of the admin interface), you'll need to:

1. Log into the admin panel
2. Select the SiteSettings record
3. Use the "Refresh settings cache" action

## Technical Details

### Settings Precedence

Settings are loaded in the following order (highest precedence first):

1. Environment variables (for critical settings like SECRET_KEY)
2. Database settings (via SiteSettings model)
3. Default values in settings.py

### Extending the System

To add new settings:

1. Add the field to the SiteSettings model
2. Update the `reload_settings` method in SettingsRegistry
3. Create migration using `python manage.py makemigrations`
4. Apply migration using `python manage.py migrate`
5. (Optional) Add a helper function to settings_service.py

### Performance

- Settings are loaded once at application startup
- All subsequent access is from cache
- Cache is invalidated when settings are updated via admin
- Default cache timeout is 1 hour (configurable)

## Troubleshooting

### Settings Not Updating

If changes to settings don't appear to take effect:

1. Check if the settings cache needs to be refreshed
2. Verify the setting is properly added to the registry
3. Restart the application if needed

### Database Migration Issues

If you encounter migration issues when adding new settings:

1. Make sure the new field has a default value
2. Check for circular import issues
3. Consider using Django's `RunPython` operation to set initial values 