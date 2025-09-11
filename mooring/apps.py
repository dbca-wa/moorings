from __future__ import unicode_literals

from django.apps import AppConfig
import sys


class MarinastayConfig(AppConfig):
    name = 'mooring'

    def ready(self):
        # Instead of calling the function, just import the module
        # where the check is registered.
        # This does NOT execute the database query immediately.
        from . import checks