from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from astroedu.activities.models import Activity
from astroedu.activities import tasks

class Command(BaseCommand):
    args = '<activity_code activity_code...>'
    option_list = BaseCommand.option_list + (
        make_option('--pdf',
            action='store_true',
            dest='pdf',
            default=False,
            help='Generate only PDF file'),
        ) + (
        make_option('--epub',
            action='store_true',
            dest='epub',
            default=False,
            help='Generate only EPUB file'),
        ) + (
        make_option('--rtf',
            action='store_true',
            dest='rtf',
            default=False,
            help='Generate only RTF files'),
        ) + (
        make_option('--zip',
            action='store_true',
            dest='zip',
            default=False,
            help='Generate ZIP file with attachments'),
        ) + (
        make_option('--thumb',
            action='store_true',
            dest='thumb',
            default=False,
            help='Generate only thumbnails'),
        ) + (
        )

    help = 'Generate downloads for an activity'

    def handle(self, *args, **options):
        options['all'] = not options['pdf'] and not options['epub'] and not options['rtf'] and not options['zip'] and not options['thumb']

        if len(args) == 0:
            self.stderr.write('No activity specified')
        
        elif len(args) == 1 and args[0] == 'all':
            self.stdout.write('Generating downloads for all activities')
            for activity in Activity.objects.all_super():
                self.stdout.write('Activity "%s"... ' % activity.code, ending='')
                _generate_downloads(activity, options)
                self.stdout.write('done.')
        
        else:
            for activity_code in args:
                try:
                    activity = Activity.objects.get(code=activity_code)
                except Activity.DoesNotExist:
                    raise CommandError('Activity "%s" does not exist' % activity_code)

                _generate_downloads(activity, options)
                self.stdout.write('Successfully generated downloads for activity "%s"' % activity_code)


def _generate_downloads(activity, options):
    if options['all'] or options['thumb']:
        tasks.make_thumbnail(activity)
    if options['all'] or options['zip']:
        tasks.zip_attachments(activity)
    if options['all'] or options['epub']:
        tasks.make_epub(activity)
    if options['all'] or options['pdf']:
        tasks.make_pdf(activity)
    # if options['all'] or options['rtf']:
    #     tasks.make_rtf(activity)
