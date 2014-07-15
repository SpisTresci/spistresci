import os

IS_DEV = True
DOMAIN_NAME = 'localhost:8000'
WWW_ROOT = 'http://%s/' % DOMAIN_NAME


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'spistresci',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
    },
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://localhost:10000/solr/masterbook_latest',
        'EXCLUDED_INDEXES': [
            'spistresci.search_indexes.BookstoreIndex',
        ]
    },

    'bookstore': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://localhost:10000/solr/bookstore_latest',
        'EXCLUDED_INDEXES': [
            'spistresci.search_indexes.MasterBookIndex',
        ]
    },

    'book_details': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://localhost:10000/solr/masterbook_with_description_latest',
        'EXCLUDED_INDEXES': [
            'spistresci.search_indexes.BookstoreIndex',
        ]
    },
}

try:
    from local import *
except ImportError:
    pass
