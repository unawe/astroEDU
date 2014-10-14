from django.core.management.base import BaseCommand, CommandError

from astroedu.activities import tasks
from astroedu.activities.models import Activity, Collection, Institution

class Command(BaseCommand):
    help = 'Generate thumnails for all activity objects'

    def handle(self, *args, **options):
        for activity in Activity.objects.all_super():
            self.stdout.write('Activity "%s"... ' % activity.code, ending='')
            tasks.make_thumbnail(activity)
            self.stdout.write('done.')
        for collection in Collection.objects.all():
            self.stdout.write('Collection "%s"... ' % collection.slug, ending='')
            tasks.make_thumbnail(collection)
            self.stdout.write('done.')
        for institution in Institution.objects.all():
            self.stdout.write('Institution "%s"... ' % institution.slug, ending='')
            tasks.make_thumbnail(institution)
            self.stdout.write('done.')

