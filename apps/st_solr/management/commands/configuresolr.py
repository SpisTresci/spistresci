from os import (
    makedirs,
    remove,
    walk,
)
from os.path import (
    abspath,
    dirname,
    exists,
    isdir,
    join,
    sep,
)
import shutil

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.conf import settings

from spistresci.apps.st_solr.constants import *
from spistresci.apps.st_solr.utils import *


class Command(BaseCommand):

    def handle(self, version=SOLR_VERSION, *args, **options):
        self.generate_configs()
        self.move_jars()
        print "configuration OK!"

    @staticmethod
    def move_jars():

        jars = [
            'lucene-libs/lucene-analyzers-morfologik-4.5.0.jar',
            'lib/morfologik-stemming-1.7.1.jar',
            'lib/morfologik-polish-1.7.1.jar',
            'lib/morfologik-fsa-1.7.1.jar',
        ]

        jars = [
            join(
                SOLR_DIR,
                'contrib/analysis-extras/',
                path_to_file
            )
            for path_to_file in jars
        ]

        mysql_connector_java = 'http://repo1.maven.org/maven2/mysql/mysql-connector-java/5.1.16/mysql-connector-java-5.1.16.jar'  # nopep8
        filename = mysql_connector_java.split('/')[-1]
        filename = join(DOWNLOAD_DIR, filename)

        if not exists(filename):
            downloadFile(mysql_connector_java, filename)

        jars.append(filename)

        for jar in jars:
            print "Copying %s to %s ..." % (jar, SOLR_DIST_DIR)

            filename = jar.split(sep)[-1]
            if not exists(join(SOLR_DIST_DIR, filename)):
                shutil.move(jar, SOLR_DIST_DIR)

    @staticmethod
    def generate_configs():

        config_directory = SOLR_CONFIGS_DIR

        if not config_directory:
            exit('Please define destination directory')

        config_directory = config_directory.rstrip(sep)
        print config_directory

        if exists(config_directory):
            print '%s %s exists. Override? [Y/N]: ' % (
                'Directory' if isdir(config_directory) else 'File',
                config_directory
            ),

            choice = raw_input().lower()
            if choice != 'y':
                return

            if isdir(config_directory):
                shutil.rmtree(config_directory)
            else:
                remove(config_directory)

        makedirs(config_directory)

        for core in SOLR_CORES:
            print "CORE: %s" % core
            configs = set()

            settings.TEMPLATE_DIRS = [
                abspath(
                    join(SOLR_BASE_TEMPLATE_DIR, '..', core)
                ),
                SOLR_BASE_TEMPLATE_DIR,
            ]

            for template_dir in settings.TEMPLATE_DIRS:
                for path, dirs, files in walk(template_dir):
                    sub_path = '%s/' % path.replace(template_dir, '')
                    for f in files:
                        #print sub_path[1:], str(f)
                        item = sub_path[1:] + f
                        configs.add(item)

            core_dir = join(config_directory, core)
            makedirs(core_dir)

            for config_file_name in configs:
                new_file_path = join(core_dir, config_file_name)

                print "Generate: %s" % (
                    new_file_path.replace(config_directory, '').lstrip(sep)
                )

                if not exists(dirname(new_file_path)):
                    makedirs(dirname(new_file_path))

                with open(new_file_path, 'w') as f:
                    f.write(
                        render_to_string(
                            config_file_name,
                            {'SOLR_DIST_DIR': SOLR_DIST_DIR},
                        )
                    )

        settings.TEMPLATE_DIRS = [
            abspath(
                join(SOLR_BASE_TEMPLATE_DIR, '..')
            ),
        ]

        solr_xml = 'solr.xml'
        solr_xml_path = join(config_directory, solr_xml)

        print "GENERAL CONFIG:"
        print "Generate: %s" % (
            solr_xml_path.replace(config_directory, '').lstrip(sep)
        )

        with open(solr_xml_path, 'w') as f:
            f.write(render_to_string(solr_xml, {'cores': SOLR_CORES}))
