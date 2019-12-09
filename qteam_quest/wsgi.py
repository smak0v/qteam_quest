"""
WSGI config for qteam_quest project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qteam_quest.settings')

application = get_wsgi_application()
