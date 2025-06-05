"""
WSGI config for ledger project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""
import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling, MediaCling

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("BASE_DIR", BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mooring.settings")
#application = get_wsgi_application()
application = Cling(MediaCling(get_wsgi_application()))



# from django.apps import apps
# from django.db import connection

# all_apps = apps.get_app_configs()

# for app in all_apps:
#     print(f"App: {app.label}")
#     for model in app.get_models():
#         table_name = model._meta.db_table
#         print(f"  Table: {table_name}")