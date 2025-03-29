"""
WSGI config for WealthPro project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Add the project directory to the Python path
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

# Set the environment variable to specify the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wealthpro.settings')

# Get the application
application = get_wsgi_application()

# For Gunicorn
app = application 