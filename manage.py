#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astroedu.settings')
    if not os.getenv('DJANGO_SETTINGS_CONFIG'):
    	sys.exit('Configuration problem: DJANGO_SETTINGS_CONFIG environment variable is not set. Exiting...')


    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

    import astroedu.startup as startup
    startup.run()
