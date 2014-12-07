#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astroedu.settings')
    # TODO: test for DJANGO_SETTINGS_CONFIG == 'DEV' or 'PROD'


    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

    import astroedu.startup as startup
    startup.run()
