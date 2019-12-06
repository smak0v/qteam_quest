import os

from django.core.exceptions import ImproperlyConfigured


def get_env_value(env_variable):
    try:
        return os.environ[env_variable]
    except KeyError:
        error_message = 'Set the {} environment variable'.format(env_variable)
        raise ImproperlyConfigured(error_message)
