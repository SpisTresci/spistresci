import os

IS_PROD = True
DOMAIN_NAME = 'alpha.spistresci.pl'
WWW_ROOT = 'http://%s/' % DOMAIN_NAME

SOLR = {
    'login':'st_' + os.getenv('ENV'),
    'pass':'zGNaEN52qfCLju0r'
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

    'book_details': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        #'URL': 'http://127.0.0.1:8983/solr/bookstore_alpha_10',
        'URL': 'http://%(login)s:%(pass)s@solr.spistresci.pl:8090/solr/masterbook_with_description_latest' % SOLR,
        'EXCLUDED_INDEXES': [
            'spistresci.search_indexes.MasterBookIndex',
        ]
    },
}

EMAIL_SUBJECT_PREFIX= '[SpisTresci][Production]'
