from django.core.management.base import BaseCommand
from django.conf import settings

from spistresci.apps.st_solr.constants import *
from spistresci.apps.st_solr.utils import *

import os
import hashlib
import shutil

class Command(BaseCommand):

    def handle(self, version=SOLR_VERSION, *args, **options):

        if version not in SOLR_VERSIONS:
            print "Please define %s SOLR version in %s" % (version, os.path.realpath(__file__))
            return

        solr_archive_file = os.path.join(DOWNLOAD_DIR, "solr-%s.zip" % version)

        if not os.path.isfile(solr_archive_file):
            url = SOLR_VERSIONS[version].get('url', SOLR_DEFAULT_DOWNLOAD_URL % {'version':version})
            downloadFile(url, solr_archive_file)

        if hashlib.md5(open(solr_archive_file).read()).hexdigest() != SOLR_VERSIONS[version]['md5']:
            print "Checksum of solr archive is wrong! Please check that!"
            return

        self.unpackSolr(solr_archive_file, PROJECT_SOLR_DIR, version)


    def unpackSolr(self, file, dir, version):
        print "Unpacking %s to %s ..." % (file, PROJECT_SOLR_DIR)
        shutil.rmtree(dir, True)
        shutil.rmtree(os.path.join(dir, '..' , '_solr/'), True)

        unpackZIP(file, dir)
        shutil.move(os.path.join(dir, 'solr-%s' % version), os.path.join(dir, '..' , '_solr/'))

        shutil.rmtree(dir)
        shutil.move(os.path.abspath(os.path.join(dir, '..' , '_solr/')), dir)
