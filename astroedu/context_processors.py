# from astroedu.activities.models import Activity
from django.conf import settings

# def featured(request):
# 	return {'featured': Activity.objects.featured()[0:2], }

def debug(request):
    return {
    	'DEBUG': settings.DEBUG, 
    	'DJANGO_SETTINGS_CONFIG': settings.DJANGO_SETTINGS_CONFIG
    }
