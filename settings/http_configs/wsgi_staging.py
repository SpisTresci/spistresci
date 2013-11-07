import os
import sys

os.environ['ENV'] = 'staging' 
sys.path.append('/home/frontend/frontend/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spistresci.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

