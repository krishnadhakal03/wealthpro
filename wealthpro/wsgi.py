import os
import sys
from pathlib import Path

# Add the project directory to the sys.path
sys.path.append('/var/www/wealthpro')
sys.path.append('/var/www/wealthpro/wealthpro')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wealthpro.settings')

# Add the project directory to the Python path (BASE_DIR)
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Get the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
