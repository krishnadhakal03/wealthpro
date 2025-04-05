#!/usr/bin/env python
"""
Django configuration diagnostic tool
"""
import os
import sys
import django

# Set up Django settings before importing other modules
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wealthpro.settings")
django.setup()

from pathlib import Path
from django.conf import settings

def check_environment():
    """Check environment variables and Django settings"""
    print("\n===== Environment and Settings =====")
    try:
        # Check debug setting
        print(f"DEBUG: {settings.DEBUG}")
        
        # Check database
        db_config = settings.DATABASES['default']
        print(f"Database Engine: {db_config['ENGINE']}")
        print(f"Database Name: {db_config['NAME']}")
        
        # Check static settings
        print(f"STATIC_URL: {settings.STATIC_URL}")
        print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
        static_root_exists = os.path.exists(settings.STATIC_ROOT)
        print(f"STATIC_ROOT exists: {static_root_exists}")
        
        # Check template settings
        print(f"Template Dirs: {settings.TEMPLATES[0].get('DIRS', [])}")
        print(f"APP_DIRS enabled: {settings.TEMPLATES[0].get('APP_DIRS', False)}")
        
        # Check installed apps
        print("\nInstalled Apps:")
        for app in settings.INSTALLED_APPS:
            print(f"  - {app}")
            
        # Check middleware
        print("\nMiddleware:")
        for middleware in settings.MIDDLEWARE:
            print(f"  - {middleware}")
        
        # Check environment variables from .env
        print("\nEnvironment Variables:")
        print(f"SECRET_KEY set: {'SECRET_KEY' in os.environ}")
        print(f"ALLOWED_HOSTS: {os.environ.get('ALLOWED_HOSTS', 'Not set in environment')}")
        print(f"EMAIL_HOST_USER: {os.environ.get('EMAIL_HOST_USER', 'Not set in environment')}")
        print(f"EMAIL_HOST_PASSWORD set: {'EMAIL_HOST_PASSWORD' in os.environ}")
        
    except Exception as e:
        print(f"Error checking environment: {e}")

def check_urls():
    """Check Django URL configuration"""
    print("\n===== URLs =====")
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        url_patterns = resolver.url_patterns
        print(f"Number of URL patterns: {len(url_patterns)}")
        
        from django.urls import reverse
        try:
            home_url = reverse('home')
            print(f"Home URL resolved to: {home_url}")
        except Exception as e:
            print(f"Could not resolve 'home' URL: {e}")
            
    except Exception as e:
        print(f"Error checking URLs: {e}")

def check_models():
    """Check app models"""
    print("\n===== Models =====")
    try:
        from django.apps import apps
        all_models = apps.get_models()
        
        print(f"Number of models: {len(all_models)}")
        print("\nModels:")
        for model in all_models:
            model_name = f"{model._meta.app_label}.{model._meta.object_name}"
            print(f"  - {model_name}")
            
    except Exception as e:
        print(f"Error checking models: {e}")

def check_views():
    """Check main app views"""
    print("\n===== Views =====")
    try:
        import main.views
        view_functions = [f for f in dir(main.views) if callable(getattr(main.views, f)) and not f.startswith('_')]
        
        print(f"Number of view functions: {len(view_functions)}")
        print("\nView functions:")
        for view in view_functions:
            print(f"  - {view}")
            
    except Exception as e:
        print(f"Error checking views: {e}")

def check_templates():
    """Check if template files exist"""
    print("\n===== Templates =====")
    try:
        base_dir = Path(__file__).resolve().parent
        template_dirs = [
            base_dir / 'main' / 'templates' / 'main',
        ]
        
        for template_dir in template_dirs:
            print(f"\nChecking templates in {template_dir}:")
            if template_dir.exists():
                templates = list(template_dir.glob('*.html'))
                for template in templates:
                    print(f"  - {template.name}")
            else:
                print(f"  Template directory does not exist!")
                
    except Exception as e:
        print(f"Error checking templates: {e}")

def check_static_files():
    """Check if static files exist"""
    print("\n===== Static Files =====")
    try:
        base_dir = Path(__file__).resolve().parent
        static_dirs = [
            base_dir / 'main' / 'static',
            base_dir / 'productionfiles',
        ]
        
        for static_dir in static_dirs:
            print(f"\nChecking static files in {static_dir}:")
            if static_dir.exists():
                css_files = list(static_dir.glob('**/*.css'))
                js_files = list(static_dir.glob('**/*.js'))
                img_files = list(static_dir.glob('**/*.{png,jpg,jpeg,gif,svg}'))
                
                print(f"  CSS files: {len(css_files)}")
                print(f"  JS files: {len(js_files)}")
                print(f"  Image files: {len(img_files)}")
            else:
                print(f"  Static directory does not exist!")
                
    except Exception as e:
        print(f"Error checking static files: {e}")

if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    print(f"Django version: {django.get_version()}")
    
    check_environment()
    check_urls()
    check_models()
    check_views()
    check_templates()
    check_static_files()
    
    print("\n===== Diagnostic Complete =====") 