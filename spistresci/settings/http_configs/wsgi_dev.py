import os
os.environ['ENV'] = 'dev'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spistresci.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

