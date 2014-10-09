# Django settings for astroedu project.
import os

import secrets


SETTINGS_DIR = os.path.dirname(__file__)
# SETTINGS_LOCAL = 'astroedu'
# PROJECT_DIR = SETTINGS_DIR[:SETTINGS_DIR.find(SETTINGS_LOCAL)]
PROJECT_DIR = os.path.dirname(SETTINGS_DIR)

ADMINS = (
    ('Bruno Rino', secrets.ADMIN_EMAIL),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'astroedu',
        'USER': 'root',
        'PASSWORD': '',
        # 'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        # 'PORT': '',                      # Set to empty string for default.
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = secrets.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secrets.EMAIL_HOST_PASSWORD
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_SUBJECT_PREFIX = '[ASTROEDU] '


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    'astroedu.iau.org',
    '37.139.7.49',
    'astroedu',
    'astroedu.local',
]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Amsterdam'
# TIME_ZONE = 'UTC'
# TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-uk'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(PROJECT_DIR), 'astroEDU_uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4$oyb$23bj+5$i#csxj=#2pw$tbookqk&c==@2#a*50*0^-db!'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    # 'astroedu.context_processors.featured',
    'astroedu.context_processors.debug',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'astroedu.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'astroedu.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',

    'south',

    # Admin
    'django.contrib.admin',
    # 'django.contrib.admindocs',
    'djangoplicity.adminhistory',

    # 'huey.djhuey',
    'djcelery',


    'django.contrib.markup',
    
    # 'markupmirror',
    # # 'django_markdown',
    # 'pagedown',

    # # 'multilingual',
    # # 'multilingual.flatpages',

    # Search
    'haystack',

    'astroedu',
    'astroedu.tests',
    'astroedu.activities',
    'filemanager',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        # send an email to the site admins on every HTTP 500 error when DEBUG=False.
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'error_log': {
            # 'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/tmp/astroedu.log',
        }
        # 'request_error': {
        #     'level': 'ERROR',
        #     # 'filters': ['require_debug_false'],
        #     'class': 'logging.FileHandler',
        #     'filename': 'request_error.log',
        # }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'error_log'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# GRAPPELLI_ADMIN_TITLE = 'astroEDU administration'

# Celery
BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_DOCUMENT_FIELD = 'text'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 50
HAYSTACK_LIMIT_TO_REGISTERED_MODELS = False

THUMBNIZER_SIZES = {
    'thumb': (334, 180, True, ), 
    'thumb2': (500, 269, True, ), 
    'epubcover': (800, 1066, True, ), 
    'logo': (0, 180, True, ), 
}
THUMBNIZER_KEYS = {
    'activities': {'formats': ['thumb', 'thumb2', 'epubcover']},
    'collections': {'formats': ['thumb', 'epubcover']},
    'institutions': {'formats': ['logo', ]},
}

REPOSITORIES = {
    'Scientix': ('Scientix', 'http://www.scientix.eu/', ),
    'OER': ('OER Commons', 'http://www.oercommons.org/', ),
    'TES': ('tes connect', 'http://www.tes.co.uk/', ),
}


DJANGO_SETTINGS_CONFIG = os.environ.get('DJANGO_SETTINGS_CONFIG', None)
if DJANGO_SETTINGS_CONFIG == 'DEV':
    #TIME_ZONE = 'Europe/Dublin'
    DEBUG = True
    TEMPLATE_DEBUG = True
    # PROJECT_DIR = '/Users/rino/Workspaces/astroEDU/'
    # STATICFILES_DIRS += (MEDIA_ROOT, )
    # debug toolbar
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
    CELERY_ALWAYS_EAGER = True  # Tasks are run synchronously
    EMAIL_SUBJECT_PREFIX = '[ASTROEDU_DEV] '

elif DJANGO_SETTINGS_CONFIG == 'PROD':
    DEBUG = False
    DATABASES['default']['USER'] = secrets.DATABASE_USER_PROD
    DATABASES['default']['PASSWORD'] = secrets.DATABASE_PASSWORD_PROD
    STATIC_ROOT = '/home/web/astroEDU_static/'
    MEDIA_ROOT = '/home/web/astroEDU_uploads/'

else:
    if DJANGO_SETTINGS_CONFIG:
        raise EnvironmentError(1, 'DJANGO_SETTINGS_CONFIG environment variable set to invalid value: %s' % DJANGO_SETTINGS_CONFIG)
    else:
        raise EnvironmentError(1, 'DJANGO_SETTINGS_CONFIG environment variable not set')


import djcelery
djcelery.setup_loader()

