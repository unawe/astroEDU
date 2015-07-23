# Django settings for astroedu project.
import os

import json

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PARENT_DIR = os.path.dirname(BASE_DIR)

SECRETS_FILE = os.path.join(BASE_DIR, 'secrets.json')
if os.path.isfile(SECRETS_FILE):
    fdata = open(SECRETS_FILE)
    secrets = json.load(fdata)
    fdata.close()
else:
    raise 'No secrets found!'

ADMINS = (
    ('Bruno Rino', secrets['ADMIN_EMAIL']),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'astroedu',
        'USER': 'root',
        'PASSWORD': '',
        # 'HOST': '',     # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        # 'PORT': '',     # Set to empty string for default.
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = secrets['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = secrets['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_SUBJECT_PREFIX = '[ASTROEDU] '

# SESSION_COOKIE_AGE = 86400  # 1 day, in seconds
# SESSION_SAVE_EVERY_REQUEST = False

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    'astroedu.iau.org',
    '188.166.45.19',
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
USE_L10N = False
DATETIME_FORMAT = 'Y-m-d H:i:s'

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PARENT_DIR, 'astroEDU_uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/tmp'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'pipeline.finders.PipelineFinder',
)

# Make this unique, and don't share it with anybody.
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets['SECRET_KEY']

# # List of callables that know how to import templates from various sources.
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# #     'django.template.loaders.eggs.Loader',
# )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    # 'astroedu.context_processors.featured',
    # 'astroedu.context_processors.debug',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

ROOT_URLCONF = 'astroedu.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'astroedu.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'django.contrib.redirects',

    # 'south',

    # Admin
    # 'django.contrib.admindocs',
    'djangoplicity.adminhistory',

    # 'huey.djhuey',
    'djcelery',


    'django_mistune',
    # 'markupmirror',
    # # 'django_markdown',
    # 'pagedown',

    # # 'multilingual',
    # # 'multilingual.flatpages',

    # Script concatenation
    'pipeline',

    'astroedu',
    'astroedu.testing',
    'astroedu.activities',
    'astroedu.search',
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
            'filename': os.path.join(PARENT_DIR, 'usr/log/astroedu-error.log'),
        },
        'default': {
            'class': 'logging.StreamHandler',
        },
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
        'django.db.backends': {
            'handlers': ['default',],
            'level': 'INFO',
        }
    }
}


MISTUNE_STYLES = {
    # 'escape': True,  # all raw html tags will be escaped.
    # 'hard_wrap': True,  # it will has GFM line breaks feature.
    'use_xhtml': True, # all tags will be in xhtml, for example: <hr />.
    # 'parse_html': True,  # parse text in block level html.
    # 'skip_style': True,
    # 'skip_html': True,
}


# Caching
USE_ETAGS = True  # Note: disable debug toolbar while testing!

# Bleach
BLEACH_ALLOWED_TAGS = ('sup', 'sub', 'br', )
BLEACH_ALLOWED_ATTRIBUTES = {}
BLEACH_ALLOWED_STYLES = {}

# Celery
BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'pickle'  # default serializer used by the decorators
CELERY_ACCEPT_CONTENT = ['pickle']  # serializers accepted by the deamon

# Pipeline
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_CSS = {
    'styles': {
        'source_filenames': (
            'css/fonts.css',
            'css/reset.css',
            'css/main.css',
            'css/media_1280.css',
            'css/media_1080.css',
            'css/media_992.css',
            'css/media_768.css',
            'css/media_600.css',
            'css/media_480.css',
        ),
        'output_filename': 'css/astroedu.min.css',
        'extra_context': {
            'media': 'screen',
        },
    },
}
PIPELINE_JS = {
    'scripts': {
        'source_filenames': [
            'js/jquery.js',
            'js/scripts.js',
        ],
        'output_filename': 'js/astroedu.min.js',
    }
}

WHOOSH_INDEX_PATH = '/tmp/whoosh_index'

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
    'Scientix': ('Scientix', 'https?://www.scientix.eu/', ),
    'OER': ('OER Commons', 'https?://www.oercommons.org/', ),
    'TES': ('tes connect', 'https?://www.tes.co.uk/', ),
}


DJANGO_SETTINGS_CONFIG = os.environ.get('DJANGO_SETTINGS_CONFIG', None)
if DJANGO_SETTINGS_CONFIG == 'DEV':
    TIME_ZONE = 'Europe/Dublin'
    DEBUG = True
    TEMPLATE_DEBUG = True
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
    DATABASES['default']['USER'] = secrets['DATABASE_USER_PROD']
    DATABASES['default']['PASSWORD'] = secrets['DATABASE_PASSWORD_PROD']
    STATIC_ROOT = os.path.join(PARENT_DIR, 'astroEDU_static')
    WHOOSH_INDEX_PATH = '/home/web/usr/whoosh_index'
    PIPELINE_JS['scripts']['source_filenames'].append('js/download-analytics.js')

else:
    if DJANGO_SETTINGS_CONFIG:
        raise EnvironmentError(1, 'DJANGO_SETTINGS_CONFIG environment variable set to invalid value: %s' % DJANGO_SETTINGS_CONFIG)
    else:
        raise EnvironmentError(1, 'DJANGO_SETTINGS_CONFIG environment variable not set')

