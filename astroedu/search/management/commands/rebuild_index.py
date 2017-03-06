from django.core.management.base import BaseCommand, CommandError

from astroedu.search import whoosh_utils


class Command(BaseCommand):
    help = 'Generate Whoosh index'

    def handle(self, *args, **options):
        whoosh_utils.rebuild_indexes()
