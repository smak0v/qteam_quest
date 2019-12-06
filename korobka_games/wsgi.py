"""
WSGI config for korobka_games project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'korobka_games.settings')

application = get_wsgi_application()
