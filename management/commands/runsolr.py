from django.core.management.base import BaseCommand
from django.conf import settings
import urllib
import urllib2
import os
import sys
import zipfile
import shutil
import hashlib


SOLR_VERSION="4.5.0"
SOLR_DEFAULT_DOWNLOAD_URL="http://archive.apache.org/dist/lucene/solr/%(version)s/solr-%(version)s.zip" % {"version":SOLR_VERSION}
SOLR_VERSIONS = {
    '4.5.0':{
        'md5':'9753f07cec0da9535522292ab1929880'
    }
}
DOWNLOAD_DIR='/tmp/'
#PROJECT_SOLR_DIR=os.path.join(settings.SITE_ROOT, 'solr/')
SITE_ROOT='/media/home/devel/spistresci.pl/repo/frontends/spistresci'
PROJECT_SOLR_DIR=os.path.join('/media/home/devel/spistresci.pl/repo/frontends/spistresci', 'solr/')

#class Command(BaseCommand):
#    pass

def handle(version='4.5.0'):#settings.SOLR_VERSION):

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

    unpackSolr(solr_archive_file, PROJECT_SOLR_DIR, version)
    configuresolr()
    rundevsolr()

    print "ok! :)"

def unpackSolr(file, dir, version):
    shutil.rmtree(dir, True)
    shutil.rmtree(os.path.join(dir, '..' , '_solr/'), True)

    unpackZIP(file, dir)
    shutil.move(os.path.join(dir, 'solr-%s' % version), os.path.join(dir, '..' , '_solr/'))

    shutil.rmtree(dir)
    shutil.move(os.path.abspath(os.path.join(dir, '..' , '_solr/')), dir)

def unpackZIP(zipname, dst_dir):
    with zipfile.ZipFile(zipname, "r") as z:
        z.extractall(dst_dir)

def downloadFile(url, file_name, progress_bar=True):
    if progress_bar:
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            p = float(file_size_dl) / file_size
            status = r"{0}  [{1:.2%}]".format(file_size_dl, p)
            status = status + chr(8)*(len(status)+1)
            sys.stdout.write(status)

        f.close()

    else:
        urllib.urlretrieve (url, file_name)


def rundevsolr():

    import subprocess

    JETTY_HOME = os.path.join(PROJECT_SOLR_DIR, 'example/')
    SOLR_CONFIGS_HOME = os.path.join(SITE_ROOT, 'solr_config/')

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


def configuresolr():

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
        shutil.move(jar, os.path.join(PROJECT_SOLR_DIR, 'dist/'))


    print "configuration OK!"


if __name__ == "__main__":
    handle()
