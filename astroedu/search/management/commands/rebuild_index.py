from django.core.management.base import BaseCommand, CommandError

# from astroedu.activities import tasks
# from astroedu.activities.models import Activity, Collection, Institution

from astroedu.search import whoosh_utils

class Command(BaseCommand):
    help = 'Generate Whoosh index'

    def handle(self, *args, **options):
        whoosh_utils.build_index()
