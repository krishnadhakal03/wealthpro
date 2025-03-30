import sys
import os
import sys
from pathlib import Path

# Add the project directory to the sys.path
sys.path.append('/var/www/wealthpro')
sys.path.append('/var/www/wealthpro/wealthpro')

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'wealthpro.settings'

# Activate the virtual environment directly by pointing to it in mod_wsgi configuration.
# This is done in the Apache config via WSGIDaemonProcess.

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wealthpro.settings')

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    print(f"Error loading WSGI application: {e}", file=sys.stderr)
    raise

