# from astroedu.activities.models import Activity
from django.conf import settings


def debug(request):
    return {
        'DEBUG': settings.DEBUG,
        'DJANGO_SETTINGS_CONFIG': settings.DJANGO_SETTINGS_CONFIG
    }
