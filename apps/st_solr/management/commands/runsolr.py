import os
import subprocess

from django.core.management.base import BaseCommand

from spistresci.apps.st_solr.constants import (
    SOLR_CONFIGS_DIR,
    SOLR_DIR,
    SOLR_VERSION,
)


class Command(BaseCommand):

    def handle(self, version=SOLR_VERSION, *args, **options):
        jetty_home = os.path.join(SOLR_DIR, 'example/')

        command_args = [
            'java',
            '-Dsolr.solr.home=%s' % SOLR_CONFIGS_DIR,
            '-Djetty.home=%s' % jetty_home,
            '-jar',
            os.path.join(SOLR_DIR, 'example/', 'start.jar'),
        ]

        print " ".join(command_args)
        os.chdir(jetty_home)

        proc = subprocess.Popen(command_args, shell=False)
        proc.communicate()

        print "ok"
