from __future__ import unicode_literals

from django.apps import AppConfig
import sys
import os


class MarinastayConfig(AppConfig):
    name = 'mooring'

    def ready(self):
        # Instead of calling the function, just import the module
        # where the check is registered.
        # This does NOT execute the database query immediately.
        from . import checks
        
        from django.conf import settings
        session_file_path = getattr(settings, 'SESSION_FILE_PATH', None)
        if session_file_path and not os.path.exists(session_file_path):
            try:
                os.makedirs(session_file_path, exist_ok=True)
                print(f"Created session directory: {session_file_path}")
            except Exception as e:
                print(f"Warning: Could not create session directory {session_file_path}: {e}")