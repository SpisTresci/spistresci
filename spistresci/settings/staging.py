import os

DEBUG = True

IS_STAGING = True
DOMAIN_NAME = 'staging.spistresci.pl'
WWW_ROOT = 'http://%s/' % DOMAIN_NAME
SSH_HOSTS = ['marta.spistresci.pl',]

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'spistresci.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'st_staging',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'NGUcIpHoz1UI',
        'HOST': 'db1.spistresci.pl',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    },
    'baza_calibre': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'baza_calibre',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'NGUcIpHoz1UI',
        'HOST': 'db1.spistresci.pl',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    },
    'st_backend': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'st_staging',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'NGUcIpHoz1UI',
        'HOST': 'db1.spistresci.pl',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://solr.spistresci.pl:8090/solr/masterbook_latest',
        'EXCLUDED_INDEXES': [
            'spistresci.search_indexes.BookstoreIndex',
        ]
    },

    'bookstore': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://solr.spistresci.pl:8090/solr/bookstore_latest',
        'EXCLUDED_INDEXES': [
            'spistresci.search_indexes.MasterBookIndex',
        ]
    },

    'book_details': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        #'URL': 'http://127.0.0.1:8983/solr/bookstore_alpha_10',
        'URL': 'http://solr.spistresci.pl:8090/solr/masterbook_with_description_latest',
        'EXCLUDED_INDEXES': [
            'spistresci.search_indexes.BookstoreIndex',
        ]
    },
}

EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
EMAIL_SUBJECT_PREFIX= '[SpisTresci][Staging]'

SITE_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

MEDIA_ROOT = '/var/www/django/uploads/'
