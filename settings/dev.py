import os

IS_DEV = True
DOMAIN_NAME = 'localhost:8000'
WWW_ROOT = 'http://%s/' % DOMAIN_NAME

SOLR = {
    'login':'st_' + os.getenv('ENV'),
    'pass':'YJSi4KJYu3J0Cbyo'
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        #'URL': 'http://127.0.0.1:8983/solr/masterbook_alpha_10',
        'URL': 'http://%(login)s:%(pass)s@solr.spistresci.pl:8090/solr/masterbook_latest' % SOLR,
        'EXCLUDED_INDEXES': [
            'spistresci.search_indexes.BookstoreIndex',
        ]
    },

    'bookstore': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        #'URL': 'http://127.0.0.1:8983/solr/bookstore_alpha_10',
        'URL': 'http://%(login)s:%(pass)s@solr.spistresci.pl:8090/solr/bookstore_latest' % SOLR,
        'EXCLUDED_INDEXES': [
            'spistresci.search_indexes.MasterBookIndex',
        ]
    },

    'book_details': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        #'URL': 'http://127.0.0.1:8983/solr/bookstore_alpha_10',
        'URL': 'http://%(login)s:%(pass)s@solr.spistresci.pl:8090/solr/masterbook_with_description_latest' % SOLR,
        'EXCLUDED_INDEXES': [
            'spistresci.search_indexes.BookstoreIndex',
        ]
    },
}
