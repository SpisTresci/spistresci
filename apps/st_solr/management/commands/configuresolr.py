
from django.core.management.base import BaseCommand
from django.conf import settings

from spistresci.apps.st_solr.constants import *
from spistresci.apps.st_solr.utils import *

import os
import hashlib
import shutil

class Command(BaseCommand):

    def handle(self, version=SOLR_VERSION, *args, **options):

        jars = ['contrib/analysis-extras/lucene-libs/lucene-analyzers-morfologik-4.5.0.jar',
                'contrib/analysis-extras/lib/morfologik-stemming-1.7.1.jar',
                'contrib/analysis-extras/lib/morfologik-polish-1.7.1.jar',
                'contrib/analysis-extras/lib/morfologik-fsa-1.7.1.jar']

        jars = [os.path.join(PROJECT_SOLR_DIR, path_to_file) for path_to_file in jars]

        mysql_connector_java = 'http://repo1.maven.org/maven2/mysql/mysql-connector-java/5.1.16/mysql-connector-java-5.1.16.jar'
        filename = mysql_connector_java.split('/')[-1]
        filename = os.path.join(DOWNLOAD_DIR, filename)

        if not os.path.exists(filename):
            downloadFile(mysql_connector_java, filename)

        jars.append(filename)

        for jar in jars:
            dst = os.path.join(PROJECT_SOLR_DIR, 'dist/')
            print "Copying %s to %s ..." % (jar, dst)
            shutil.move(jar, dst)


        print "configuration OK!"
