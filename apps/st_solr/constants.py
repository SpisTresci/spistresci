from django.conf import settings
import os


SOLR_VERSION = getattr(settings, 'ST_SOLR_VERSION', '4.5.0')

SOLR_DEFAULT_DOWNLOAD_URL="http://archive.apache.org/dist/lucene/solr/%(version)s/solr-%(version)s.zip" % {"version":SOLR_VERSION}
SOLR_VERSIONS = {
    '4.5.0':{
        'md5':'9753f07cec0da9535522292ab1929880'
    }
}

PROJECT_SOLR_DIR = getattr(settings, 'ST_SOLR_DIR ', os.path.abspath(os.path.join(getattr(settings, 'SITE_ROOT'), 'solr/')))

DOWNLOAD_DIR=getattr(settings, 'ST_SOLR_DOWNLOAD_DIR', '/tmp/')
