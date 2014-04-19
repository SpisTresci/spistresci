from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess
import os
from spistresci.apps.st_solr.constants import *

class Command(BaseCommand):

    def handle(self, version=SOLR_VERSION, *args, **options):
        JETTY_HOME = os.path.join(SOLR_DIR, 'example/')

        command_args = ['java',
                        '-Dsolr.solr.home=%s' % SOLR_CONFIGS_DIR,
                        '-Djetty.home=%s' % JETTY_HOME,
                        '-jar',
                        os.path.join(SOLR_DIR,'example/', 'start.jar')
                       ]

        print " ".join(command_args)
        os.chdir(JETTY_HOME)

        proc = subprocess.Popen(command_args, shell=False)
        proc.communicate()

        print "ok"
