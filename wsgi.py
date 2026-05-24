import os
import sys
from pathlib import Path

# Add project directory to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'epms.settings')

# Get Django WSGI application
application = get_wsgi_application()

# Wrap application with WhiteNoise for static file serving in production
application = WhiteNoise(application, root=str(BASE_DIR / 'staticfiles'), max_age=31536000)
