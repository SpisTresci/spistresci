import os
from os.path import join, abspath, exists, isdir, dirname
import hashlib
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


    def move_jars(self):
        jars = ['contrib/analysis-extras/lucene-libs/lucene-analyzers-morfologik-4.5.0.jar',
                'contrib/analysis-extras/lib/morfologik-stemming-1.7.1.jar',
                'contrib/analysis-extras/lib/morfologik-polish-1.7.1.jar',
                'contrib/analysis-extras/lib/morfologik-fsa-1.7.1.jar']

        jars = [os.path.join(SOLR_DIR, path_to_file) for path_to_file in jars]

        mysql_connector_java = 'http://repo1.maven.org/maven2/mysql/mysql-connector-java/5.1.16/mysql-connector-java-5.1.16.jar'
        filename = mysql_connector_java.split('/')[-1]
        filename = os.path.join(DOWNLOAD_DIR, filename)

        if not os.path.exists(filename):
            downloadFile(mysql_connector_java, filename)

        jars.append(filename)

        for jar in jars:
            print "Copying %s to %s ..." % (jar, SOLR_DIST_DIR)

            filename = jar.split(os.path.sep)[-1]
            if not os.path.exists(os.path.join(SOLR_DIST_DIR, filename)):
                shutil.move(jar, SOLR_DIST_DIR)


    def generate_configs(self):

        config_directory = SOLR_CONFIGS_DIR

        if not config_directory:
            exit('Please define destination directory')

        config_directory = config_directory.rstrip(os.path.sep)
        print config_directory

        if exists(config_directory):
            print '%s %s exists. Override? [Y/N]: ' % ('Directory' if isdir(config_directory) else 'File', config_directory),
            choice = raw_input().lower()
            if choice != 'y':
                return

            if isdir(config_directory):
                shutil.rmtree(config_directory)
            else:
                os.remove(config_directory)

        os.makedirs(config_directory)

        for core in SOLR_CORES:
            print "CORE: %s" % core
            configs = set()

            settings.TEMPLATE_DIRS = [abspath(join(SOLR_BASE_TEMPLATE_DIR, '..', core)),
                                      SOLR_BASE_TEMPLATE_DIR,]

            for template_dir in settings.TEMPLATE_DIRS:
                for path, dirs, files in os.walk(template_dir):
                    subpath = '%s/' % path.replace(template_dir, '')
                    for f in files:
                        #print subpath[1:], str(f)
                        item = subpath[1:] + f
                        configs.add(item)

            core_dir = join(config_directory, core)
            os.makedirs(core_dir)

            for config_file_name in configs:
                new_file_path = join(core_dir, config_file_name)

                print "Generate: %s" % new_file_path.replace(config_directory, '').lstrip(os.sep)

                if not exists(dirname(new_file_path)):
                    os.makedirs(dirname(new_file_path))

                with open(new_file_path, 'w') as file:
                    file.write(render_to_string(config_file_name, {'SOLR_DIST_DIR':SOLR_DIST_DIR}))


        settings.TEMPLATE_DIRS = [abspath(join(SOLR_BASE_TEMPLATE_DIR, '..')),]

        solr_xml = 'solr.xml'
        solr_xml_path = join(config_directory, solr_xml)

        print "GENERAL CONFIG:\nGenerate: %s" % solr_xml_path.replace(config_directory, '').lstrip(os.sep)
        with open(solr_xml_path, 'w') as file:
            file.write(render_to_string(solr_xml, {'cores':SOLR_CORES}))