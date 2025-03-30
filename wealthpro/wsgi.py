import sys
import os

# Add the project directory to the sys.path
sys.path.append('/var/www/wealthpro')
sys.path.append('/var/www/wealthpro/wealthpro')

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'wealthpro.settings'

# Activate the virtual environment directly by pointing to it in mod_wsgi configuration.
# This is done in the Apache config via WSGIDaemonProcess.

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

