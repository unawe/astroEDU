import os
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from astroedu.activities.models import Activity, Attachment
# from astroedu.activities import tasks

class Command(BaseCommand):
    # args = None
    option_list = BaseCommand.option_list + (
        make_option('--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete orphaned attachments'),
        )

    help = 'Find all orphaned attachments'

    def handle(self, *args, **options):
        basepath = os.path.join(settings.MEDIA_ROOT, 'activities', 'attach')
        all_files = []
        for root, dirs, files in os.walk(basepath):
            localroot = root[len(settings.MEDIA_ROOT):]
            localroot = localroot[1:] if localroot[0] == '/' else localroot
            all_files += [os.path.join(localroot, name) for name in files]

        for obj in Attachment.objects.all():
            if obj.file.name in all_files:
                all_files.remove(obj.file.name)

        orphans = all_files

        if not orphans:
            print 'No orphan attachments.'
        else:
            print 'orphan files: ', len(orphans)
            space = 0
            for obj in orphans:
                name = os.path.join(settings.MEDIA_ROOT, obj)
                print name
                space += os.path.getsize(name)
                if options['delete']:
                    os.remove(name)
            if options['delete']:
                print 'Bytes freed: ', space
            else:
                print 'Bytes wasted: ', space
