import os

DEBUG = False

IS_STAGING = True
DOMAIN_NAME = 'alpha.spistresci.pl'
WWW_ROOT = 'http://%s/' % DOMAIN_NAME


GOOGLE_ANALYTICS_ID = 'UA-45133188-1'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('Krzysztof Szumny', 'kszumny@spistresci.pl'),
    ('Piotr Zawislak', 'pzawislak@spistresci.pl'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'django_spistresci_alpha_10',  # Or path to database file if using sqlite3.
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
        'NAME': 'st',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

SOLR = {
    'login':'st_' + os.getenv('ENV'),
    'pass':'WcCPFemapxqyN4xo'
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://%(login)s:%(pass)s@solr.spistresci.pl:8090/solr/masterbook_latest' % SOLR,
        'EXCLUDED_INDEXES': [
            'spistresci.search_indexes.BookstoreIndex',
        ]
    },

    'bookstore': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://%(login)s:%(pass)s@solr.spistresci.pl:8090/solr/bookstore_latest' % SOLR,
        'EXCLUDED_INDEXES': [
            'spistresci.search_indexes.MasterBookIndex',
        ]
    },
}

EMAIL_SUBJECT_PREFIX= '[SpisTresci][Staging]'

SITE_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

import shutil, sys
if len(sys.argv) >=2 and sys.argv[1] == 'syncdb':
    shutil.copyfile(os.path.join(SITE_ROOT,'fixtures/authentication-production.json'), os.path.join(SITE_ROOT,'../initial_data.json'))
