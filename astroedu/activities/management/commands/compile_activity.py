from django.core.management.base import BaseCommand, CommandError
from astroedu.activities.models import Activity
from astroedu.activities import tasks

class Command(BaseCommand):
    args = '<activity_slug activity_slug...>'
    help = 'Generate all downloads for an activity'

    def handle(self, *args, **options):
        if len(args) == 1 and args[0] == 'all':
            self.stdout.write('Generating downloads for all activities')
            for activity in Activity.objects.all():
                self.stdout.write('Activity "%s"... ' % activity.slug, ending='')
                tasks.make_thumbnail(activity)
                activity.generate_downloads(blocking=True)
                self.stdout.write('done.')
        else:
            for activity_slug in args:
                try:
                    activity = Activity.objects.get(slug=activity_slug)
                except Activity.DoesNotExist:
                    raise CommandError('Activity "%s" does not exist' % activity_slug)

                tasks.make_thumbnail(activity)
                activity.generate_downloads(blocking=True)

                self.stdout.write('Successfully generated downloads for activity "%s"' % activity_slug)

