# Django settings for astroedu project.
import os
import sys
import json
import copy
import operator


SHORT_NAME = 'astroedu'
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PARENT_DIR = os.path.dirname(BASE_DIR)

sys.path.append(os.path.join(PARENT_DIR, 'django-apps'))

SECRETS_FILE = os.path.join(BASE_DIR, 'secrets.json')
if os.path.isfile(SECRETS_FILE):
    fdata = open(SECRETS_FILE)
    secrets = json.load(fdata)
    fdata.close()
else:
    raise 'No secrets found!'


DEBUG = False
DJANGO_SETTINGS_CONFIG = os.environ.get('DJANGO_SETTINGS_CONFIG', None)
if DJANGO_SETTINGS_CONFIG == 'DEV':
    DEBUG = True

# cannonical base URL for the website
SITE_URL = 'http://astroedu.iau.org'
SITE_ID = 1

ADMINS = (
    ('Vaclav Ehrlich', secrets['ADMIN_EMAIL']),
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets['SECRET_KEY']

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    'astroedu.iau.org',
    '188.166.45.19',
    'astroedu',
    'astroedu.local',
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.redirects',

    # Admin
    # 'django.contrib.admindocs',
    # 'djangoplicity.adminhistory',

    'pipeline',

    'parler',
    'ckeditor',

    'sorl.thumbnail',

    'django_mistune',

    'django_ext',
    'smartpages',
    'institutions',
    'activities',
    'astroedu',
    'astroedu.testing',
    'astroedu.search',
    'filemanager',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'CacheMiddleware'
    'django.middleware.locale.LocaleMiddleware',  # see https://docs.djangoproject.com/en/1.8/topics/i18n/translation/#how-django-discovers-language-preference
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'astroedu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # debug, sql_queries
                'django.template.context_processors.debug',
                # request
                'django.template.context_processors.request',
                # user, perms
                'django.contrib.auth.context_processors.auth',
                # messages, DEFAULT_MESSAGE_LEVELS
                'django.contrib.messages.context_processors.messages',
                # LANGUAGES, LANGUAGE_CODE
                'django.template.context_processors.i18n',
                # THUMBNAIL_ALIASES
                'django_ext.context_processors.thumbnail_aliases',
                # SITE_URL
                'django_ext.context_processors.site_url',
            ],
            'debug': False,
        },
    },
]

WSGI_APPLICATION = 'astroedu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'astroedu',
        'USER': secrets['DATABASE_USER_PROD'],
        'PASSWORD': secrets['DATABASE_PASSWORD_PROD'],
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = (
    # ('cs', 'Czech'),
    # ('nl', 'Dutch'),
    ('en', 'English'),
    # ('fr', 'French'),
    # ('de', 'German'),
    # ('el', 'Greek'),
    ('it', 'Italian'),
    # ('pl', 'Polish'),
    # ('ro', 'Romanian'),
    # ('es', 'Spanish'),
    # ('pt', 'Portuguese'),
    ('kr', 'Korean'),
)
LANGUAGES = sorted(LANGUAGES, key=operator.itemgetter(0))

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

USE_L10N = True
FORMAT_MODULE_PATH = (
    'formats',
)
# DATETIME_FORMAT = 'Y-m-d H:i:s'

USE_TZ = True

# Media

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PARENT_DIR, 'astroedu_uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PARENT_DIR, 'astroedu_static')

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
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'pipeline.finders.PipelineFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# parler
# http://django-parler.readthedocs.org/en/latest/
# https://github.com/edoburu/django-parler
PARLER_LANGUAGES = {
    SITE_ID: (
        {'code': 'en'},
        {'code': 'it'},
        {'code': 'kr'},
    ),
    'default': {
        'fallbacks': ['en'],
        'hide_untranslated': True,   # False is the default; let .active_translations() return fallbacks too.
    }
}

# Email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = secrets['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = secrets['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_SUBJECT_PREFIX = '[astroedu] '


# Caching
USE_ETAGS = True  # Note: disable debug toolbar while testing!

# Pipeline
PIPELINE = {
    # 'PIPELINE_ENABLED': True,
    # 'JS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    # 'CSS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    'STYLESHEETS': {
        'styles': {
            'source_filenames': [
                'css/fonts.css',
                'css/reset.css',
                'css/main.css',
                'css/media_1280.css',
                'css/media_1080.css',
                'css/media_992.css',
                'css/media_768.css',
                'css/media_600.css',
                'css/media_480.css',
            ],
            'output_filename': 'css/astroedu.min.css',
            'extra_context': {
                'media': 'screen',
            },
        },
    },
    'JAVASCRIPT': {
        'scripts': {
            'source_filenames': [
                'js/jquery.js',
                'js/scripts.js',
            ],
            'output_filename': 'js/astroedu.min.js',
        }
    },
}

# # Thumbnails
# # http://sorl-thumbnail.readthedocs.org/en/latest/reference/settings.html
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
THUMBNAIL_DBM_FILE = os.path.join(PARENT_DIR, 'usr/redis/thumbnails_astroedu')
# THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.convert_engine.Engine'  #TODO: revisit this choice
THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.pil_engine.Engine'  #TODO: revisit this choice
THUMBNAIL_KEY_PREFIX = 'sorl-thumbnail-astroedu'
THUMBNAIL_PRESERVE_FORMAT = 'True'
# # THUMBNAIL_ALTERNATIVE_RESOLUTIONS = [1.5, 2]
THUMBNAIL_ALIASES = {
    'thumb': '334x180',
    'thumb2': '500x269',
    'epubcover': '800x1066',
    'logo': 'x180',
}


# CK editor
CKEDITOR_UPLOAD_PATH = 'upload/'
CKEDITOR_CONFIGS = {
    ## see http://docs.cksource.com/CKEditor_3.x/Developers_Guide/Toolbar
    'smartpages': {
        'fillEmptyBlocks': False,
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Source', ],
            ['Format', ],
            ['Bold', 'Italic', '-', 'Underline', 'Subscript', 'Superscript', '-', 'Undo', 'Redo', 'RemoveFormat', ],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', ],
            ['Link', 'Unlink', ],
            ['Image', 'Table', 'SpecialChar', ],
            ['Maximize', 'ShowBlocks', ],
            ['BidiLtr', 'BidiRtl', ],
        ],
        'width': 845,
    },
    'small': {
        'fillEmptyBlocks': False,
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Source', ],
            ['Bold', 'Italic', '-', 'Subscript', 'Superscript', '-', 'Undo', 'Redo', 'RemoveFormat', ],
            ['Link', 'Unlink', ],
            # ['Image', ],
            ['BidiLtr', 'BidiRtl', ],
        ],
        'height': 100,
    },

}

# Bleach
BLEACH_ALLOWED_TAGS = ('sup', 'sub', 'br', )
BLEACH_ALLOWED_ATTRIBUTES = {}
BLEACH_ALLOWED_STYLES = {}

# Mistune
MISTUNE_STYLES = {
    # 'escape': True,  # all raw html tags will be escaped.
    # 'hard_wrap': True,  # it will has GFM line breaks feature.
    'use_xhtml': True,  # all tags will be in xhtml, for example: <hr />.
    # 'parse_html': True,  # parse text in block level html.
    # 'skip_style': True,
    # 'skip_html': True,
}

# Woosh Search
WHOOSH_INDEX_PATH = '/home/web/usr/whoosh_index/astroedu'


# SESSION_COOKIE_AGE = 86400  # 1 day, in seconds
# SESSION_SAVE_EVERY_REQUEST = False


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
            'handlers': ['default', ],
            'level': 'INFO',
        }
    }
}

ACTIVITY_DOWNLOADS = {
    'model': 'activities.models.Activity',
    'filename_tpl': '%(slug)s-astroEDU-%(code)s%(lang)s.%(ext)s',
    'path': 'activities/download/',
    'renderers': {
        'pdf': 'astroedu.renderers.activity.pdf',
        'rtf': 'astroedu.renderers.activity.rtf',
        'epub': 'astroedu.renderers.activity.epub',
        'zip': 'astroedu.renderers.activity.zip',
    }
}


REPOSITORIES = {
    'Scientix': ('Scientix', 'https?://www.scientix.eu/', ),
    'OER': ('OER Commons', 'https?://www.oercommons.org/', ),
    'TES': ('tes connect', 'https?://www.tes.co.uk/', ),
}


if DJANGO_SETTINGS_CONFIG == 'DEV':
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    # TIME_ZONE = 'Europe/Dublin'
    STATIC_ROOT = '/tmp'
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
    EMAIL_SUBJECT_PREFIX = '[astroedu dev] '

    THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.dbm_kvstore.KVStore'  # in-memory sorl KV store
    THUMBNAIL_DUMMY = True
    # THUMBNAIL_DUMMY_SOURCE = 'http://placekitten.com/%(width)s/%(height)s'
    # THUMBNAIL_DUMMY_SOURCE = 'http://placehold.it//%(width)sx%(height)s'
    # THUMBNAIL_DUMMY_RATIO = 1.5

    WHOOSH_INDEX_PATH = os.path.join(PARENT_DIR, 'usr/whoosh_index/astroedu')

elif DJANGO_SETTINGS_CONFIG == 'PROD':
    DEBUG = False
    PIPELINE['JAVASCRIPT']['scripts']['source_filenames'].append('js/download-analytics.js')

else:
    if DJANGO_SETTINGS_CONFIG:
        raise EnvironmentError(1, 'DJANGO_SETTINGS_CONFIG environment variable set to invalid value: %s' % DJANGO_SETTINGS_CONFIG)
    else:
        raise EnvironmentError(1, 'DJANGO_SETTINGS_CONFIG environment variable not set')
