from django.conf import settings
from os.path import  join, abspath, dirname

SOLR_CORES = [
    'bookstore_latest',
    'bookstore_latest_bis',

    'masterbook_latest',
    'masterbook_latest_bis',
]

SOLR_VERSION = getattr(settings, 'ST_SOLR_VERSION', '4.5.0')

SOLR_DEFAULT_DOWNLOAD_URL="http://archive.apache.org/dist/lucene/solr/%(version)s/solr-%(version)s.zip" % {"version":SOLR_VERSION}
SOLR_VERSIONS = {
    '4.5.0':{
        'md5':'9753f07cec0da9535522292ab1929880'
    }
}

SOLR_DIR = getattr(settings, 'ST_SOLR_DIR ', abspath(join(getattr(settings, 'SITE_ROOT'), 'solr/')))
SOLR_CONFIGS_DIR = join(SOLR_DIR, 'configs/')

DOWNLOAD_DIR=getattr(settings, 'ST_SOLR_DOWNLOAD_DIR', '/tmp/')

SOLR_DIST_DIR = join(SOLR_DIR, 'dist/') if True else '/opt/solr/dist/'


SOLR_BASE_TEMPLATE_DIR = abspath(join(dirname(__file__), 'templates/_base/'))