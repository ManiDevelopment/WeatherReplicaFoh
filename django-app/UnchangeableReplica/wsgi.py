# You should not edit this file
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UnchangeableReplica.settings')

application = get_wsgi_application()
