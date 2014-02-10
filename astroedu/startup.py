from django.conf import settings

def dev():
    DEV_DOMAIN = 'localhost:8002'
    from django.contrib.sites.models import Site
    current_site = Site.objects.get_current()
    if current_site.domain != DEV_DOMAIN:
        current_site.domain = DEV_DOMAIN
        print 'updating current_site.domain...'
        current_site.save()


def run():
    'Code executed on django startup; technique used by Pinax'
    if settings.DEBUG and settings.DJANGO_SETTINGS_CONFIG == 'DEV':
        dev()
