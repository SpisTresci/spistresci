from settings import *
import os
DEBUG = False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('Anita Wysokinska', 'awysokinska@spistresci.pl'),
    ('Krzysztof Szumny', 'kszumny@spistresci.pl'),
    ('Piotr Zawislak', 'pzawislak@spistresci.pl'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'django_alpha_5',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://solr1.spistresci.pl:8090/solr1/alpha6',
        'EXCLUDED_INDEXES': [
            'main_service.search_indexes.BookstoreIndex',
        ]
    },

    'bookstore': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://solr1.spistresci.pl:8090/solr1/bookstore-alpha6',
        'EXCLUDED_INDEXES': [
            'main_service.search_indexes.MasterBookIndex',
        ]
    },

}



EMAIL_SUBJECT_PREFIX= 'Welcome Screen:'

#Note: This seems to be stupid, but in production mode template dir should be absolute path :/
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT,'templates'),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
#MEDIA_ROOT = '/home/frontend/frontend/imgs'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
#MEDIA_URL = ''
