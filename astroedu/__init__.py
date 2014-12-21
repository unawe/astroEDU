# these environment variables must be defined before celery
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astroedu.settings')
os.environ.setdefault('DJANGO_SETTINGS_CONFIG', 'PROD')

# This will make sure the celery app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
