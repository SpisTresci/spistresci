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
        'URL': 'http://localhost:8983/solr/masterbook',
    },
}

try:
    from local import *
except ImportError:
    pass
