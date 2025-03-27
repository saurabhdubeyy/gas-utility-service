"""
WSGI config for Render deployment
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gas_utility_service.settings')

# This application object is used by the Render WSGI server
application = get_wsgi_application() 