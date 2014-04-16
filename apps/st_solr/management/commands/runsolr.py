from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess

from spistresci.apps.st_solr.constants import *

class Command(BaseCommand):

    def handle(self, version=SOLR_VERSION, *args, **options):

        JETTY_HOME = os.path.join(PROJECT_SOLR_DIR, 'example/')
        SOLR_CONFIGS_HOME = os.path.join(os.path.join(getattr(settings, 'SITE_ROOT')), 'solr_config/')

        command_args = ['java',
                        '-Dsolr.solr.home=%s' % SOLR_CONFIGS_HOME,
                        '-Djetty.home=%s' % JETTY_HOME,
                        '-jar',
                        os.path.join(PROJECT_SOLR_DIR,'example/', 'start.jar')
                       ]

        print " ".join(command_args)
        os.chdir(JETTY_HOME)

        proc = subprocess.Popen(command_args, shell=False)
        proc.communicate()

        print "ok"
