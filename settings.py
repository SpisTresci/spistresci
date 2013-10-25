# Django settings for main_service project.
import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'django_spistresci_dev',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    },
    'baza_calibre': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'baza_calibre',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    },
    'st_backend': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'st_devel',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

DATABASE_ROUTERS = [
    'spistresci.db_routers.DBRouter',
]

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Warsaw'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pl'

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
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/var/www/django/static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT,'static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8=u8p9csxz_0@%6rc2%0h(r_+7kj+2kb06lyu1)w4v^$jdf@sg'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'spistresci.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'spistresci.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT,'templates/'),
    os.path.join(SITE_ROOT,'../common/templates/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
     'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    'spistresci',
    'haystack',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # allauth providers
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'registration',
    'django_common',
    "django_cron",
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
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
HAYSTACK_LIMIT_TO_REGISTERED_MODELS = False
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        #'URL': 'http://127.0.0.1:8983/solr/masterbook_alpha_10',
        'URL': 'http://solr.spistresci.pl:8090/solr/masterbook_latest',
        'EXCLUDED_INDEXES': [
            'spistresci.search_indexes.BookstoreIndex',
        ]
    },

    'bookstore': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        #'URL': 'http://127.0.0.1:8983/solr/bookstore_alpha_10',
        'URL': 'http://solr.spistresci.pl:8090/solr/bookstore_latest',
        'EXCLUDED_INDEXES': [
            'spistresci.search_indexes.MasterBookIndex',
        ]
    },
}

AUTHENTICATION_BACKENDS = {
     'spistresci.auth_backends.eGazeciarzAuthenticationBackend',
     'allauth.account.auth_backends.AuthenticationBackend',
     'django.contrib.auth.backends.ModelBackend',
}

TEMPLATE_CONTEXT_PROCESSORS = {
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
}

# SOCIALACCOUNT_PROVIDERS are needed for social authentication, which is currently implemented using django-allauth.
# Each provider needs to be defined in INSTALLED_APPS, and usually require inserting to database special information
# about secret key/app id of particular provider, which is done by django-fixtures loaded dynamically in settings file

SOCIALACCOUNT_PROVIDERS = {
    'facebook':
    {
        'SCOPE': ['email'],
        'AUTH_PARAMS': { 'auth_type': 'https' },
        'METHOD': 'oauth2' ,
        'LOCALE_FUNC': lambda request: 'pl-pl',
    },
    'google':
    {
        'SCOPE': ['https://www.googleapis.com/auth/userinfo.profile', 'email'],
        'AUTH_PARAMS': { 'access_type': 'online' },
    },
    'twitter':
    {
        'SCOPE': ['r_emailaddress'],
    },
}

ACCOUNT_ACTIVATION_DAYS = 5

# NOTE: for local tests you can use backend from django_common, which save email as a file
# EMAIL_BACKEND = 'django_common.email_backends.CustomFileEmailBackend'
# EMAIL_FILE_PATH = '/home/mateusz/tmp/messages'
# EMAIL_FILE_EXT = 'eml'

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'spistresci'
EMAIL_HOST_PASSWORD = 'spistresci-rules!1'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = 'no-reply@spistresci.pl'

CRON_CLASSES = [
    "spistresci.cron.TrackNotificationCronJob",
    "spistresci.cron.ClearUsersCronJob",
]
import shutil, sys
if len(sys.argv) >=2 and sys.argv[1] == 'syncdb':
    shutil.copyfile(os.path.join(SITE_ROOT,'fixtures/authentication-dev.json'), os.path.join(SITE_ROOT,'../initial_data.json'))
