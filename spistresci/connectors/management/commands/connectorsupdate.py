# -*- coding: utf-8 -*-

import os
from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.timezone import now
from spistresci.connectors.management.commands._base import ConnectorsCommandBase

from spistresci.connectors.generic.GenericConnector import GenericConnector
from spistresci.connectors.utils.ConfigReader import ConfigReader
from spistresci.connectors.utils.ConnectorsLogger import logger_instance
from spistresci.models import (
    BookstoreCommandStatus,
    CommandStatus,
)


class Command(BaseCommand, ConnectorsCommandBase):
    """
    Data of each service/bookstore has to be updated regularly.

    This command triggers mechanism, and following thing are happening:

     1. data in xml/json/marc21 format are downloaded for specified bookstores
     2. if bookstore provides compressed data, data is unpacked
     3. unpacked data are moved to 'data/[serivce_name]' directory
     4. data are added to git service submodule directory

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

        cmd_status = CommandStatus()
        cmd_status.save()

        for connector in connectors:
            try:

                self.run_connector_method(
                    connector,
                    connector.fetchData,
                    BookstoreCommandStatus.TYPE_FETCH,
                    cmd_status,
                )

                self.run_connector_method(
                    connector,
                    connector.parse,
                    BookstoreCommandStatus.TYPE_PARSE,
                    cmd_status,
                )

                self.run_connector_method(
                    connector,
                    connector.analyze,
                    BookstoreCommandStatus.TYPE_ANALYZE,
                    cmd_status,
                )

            except:
                self.logger.exception(
                    'Update of connector %s FAILED' % connector.name
                )
            else:
                self.logger.debug(
                    'Update of connector %s FINISHED :)' % connector.name
                )

        cmd_status.finished = True
        cmd_status.success = True
        cmd_status.end = now()
        cmd_status.save()

        self.logger.debug('Execution finished')

    def run_connector_method(self, connector, method, cmd_type, cmd_status):
        """
        Wrote to run one of the few special methods like connector.fetchData,
        connector.parse or connector.merge. This method care about saving
        status of command, what is needed to prepare data for analyze on:
        http://spistresci.pl/monitor/
        """

        bookstore_cmd_status = BookstoreCommandStatus(
            cmd_status=cmd_status,
            bookstore=connector.bookstore,
            type=cmd_type,
        )
        bookstore_cmd_status.save()
        connector.bookstore_cmd_status = bookstore_cmd_status

        try:
            method()
            bookstore_cmd_status.success = True

        except Exception as e:

            self.logger.exception(
                'Error executing %s in connector %s' % (
                    cmd_type,
                    connector.name
                )
            )

            raise e

        finally:
            bookstore_cmd_status.finished = True
            bookstore_cmd_status.end = now()
            bookstore_cmd_status.save()
