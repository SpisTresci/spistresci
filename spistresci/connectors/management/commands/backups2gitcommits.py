# -*- coding: utf-8 -*-

import glob
import os
import tarfile
from datetime import datetime
from optparse import make_option
from shutil import copytree, rmtree
from tarfile import ReadError

from django.conf import settings
from django.core.management.base import BaseCommand

from git import Repo
from spistresci.connectors.generic.GenericConnector import GenericConnector
from spistresci.connectors.management.commands. \
    _base import ConnectorsCommandBase
from spistresci.connectors.utils.ConfigReader import ConfigReader
from spistresci.connectors.utils.ConnectorsLogger import logger_instance


def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        rmtree(to_path)
    copytree(from_path, to_path)


class Command(BaseCommand, ConnectorsCommandBase):
    """
    Downloaded data for all bookstores are specific. Most of the time only part
    of data changes. This happen, because changes occurs only in case of
    correction in title or other matadata, or in case of changed price.

    This has the effect that difference between two 20 MB xml files from two
    different days can differs only by 1000 characters (~1KB). In that case,
    it is good idea to store base file as initial commit, and later further
    changes as further git commits.

    In first 'backup-data' implementation all data were stored in compressed
    tar.bz2 files. This management command was provided to give possibility of
    converting old type of backuped date, to new one.

    Note: there is other 'gitcommits2backups' management command, which converts
    git commits to tar.bz2 archives
    """

    help = __doc__

    option_list = BaseCommand.option_list + (
        make_option(
            '--mode',
            action='store',
            dest='mode',
            help=
                'Command can be run in few different modes. Each mode has its '
                'own configuration file in: {}. Available modes: {}. '
                'Default mode: {}.'.format(
                    os.path.join(ConfigReader.CONF_DIR, '[mode].ini'),
                    ', '.join(ConfigReader.get_list_of_configs()),
                    'update'
                ),
            type='choice',
            default='update',
            choices=ConfigReader.get_list_of_configs(),
        ),
    )

    def __init__(self):
        super(Command, self).__init__()
        self.logger = None

    def handle(self, *args, **options):

        GenericConnector.config_file = os.path.join(
            settings.SITE_ROOT,
            'conf',
            '%s.ini' % options['mode']
        )

        connectors, partial = self.get_list_of_connectors_to_run()

        self.logger = logger_instance(
            os.path.join(
                settings.SITE_ROOT,
                GenericConnector.config_object.get('DEFAULT', 'log_config')
            )
        )

        self.logger.debug(
            'Created following connectors %s' % [
                connector.name
                for connector in connectors
            ]
        )

        for connector in connectors:
            print connector.name

            data_dir = os.path.join(
                settings.SITE_ROOT, '..', 'data', connector.name
            )
            xml_dir = os.path.join(data_dir, 'xml')
            log_dir = os.path.join(data_dir, 'log')

            if not os.path.exists(os.path.join(data_dir, '.git/')):
                repo = Repo.init(data_dir)
                os.makedirs(log_dir)
            else:
                repo = Repo(data_dir)

            archive_dir = os.path.join(
                settings.SITE_ROOT, '..', 'backup', connector.name.lower()
            )
            os.chdir(archive_dir)

            archive_names = glob.glob("*.tar.bz2")
            archive_names.sort()

            for archive_name in archive_names:
                unpacked_data_dir = archive_name.replace('.tar.bz2', '')

                commit_date = datetime.strptime(unpacked_data_dir, '%Y%m%d%H%M%S')
                commit_date_str = commit_date.strftime("%Y-%m-%d %H:%M:%S")

                try:
                    tar = tarfile.open(archive_name)
                    tar.extractall()
                    tar.close()

                    connector.backup_dir = os.path.join(
                        settings.SITE_ROOT, '..', 'backup', connector.name.lower(), unpacked_data_dir
                    )

                    connector.unpack_dir = connector.backup_dir

                    connector.unpackData(delete_archive=True)

                except ReadError, e:
                    with open(os.path.join(data_dir, 'log', 'errors.log'), 'w+') as f:
                        msg = "File %s: %s" % (archive_name, str(e))
                        print >> f, msg,
                    commit_msg = msg
                else:
                    copy_and_overwrite(unpacked_data_dir, xml_dir)
                    rmtree(unpacked_data_dir)
                    commit_msg = "Service: %s\nDate: %s" % (connector.name, commit_date_str)

                repo.index.add(['xml', 'log'])

                os.environ["GIT_AUTHOR_DATE"] = \
                    os.environ["GIT_COMMITTER_DATE"] = commit_date_str

                repo.index.commit(commit_msg)

                repo.create_tag(commit_date.strftime('%Y-%m-%d'))

        self.logger.debug('Execution finished')
