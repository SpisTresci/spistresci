# -*- coding: utf-8 -*-

import os
from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.timezone import now
from spistresci.connectors import Tools
from spistresci.connectors.generic.GenericConnector import GenericConnector
from spistresci.connectors.utils.ConfigReader import ConfigReader
from spistresci.connectors.utils.ConnectorsLogger import logger_instance
from spistresci.models import (
    BookstoreCommandStatus,
    CommandStatus,
)


def get_list_of_configs():
    return ['update', 'test']


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            '--mode',
            action='store',
            dest='mode',
            help='Mode',
            type='choice',
            default='update',
            choices=get_list_of_configs(),
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

                # self.run_connector_method(
                #     connector,
                #     connector.parse,
                #     BookstoreCommandStatus.TYPE_PARSE,
                #     cmd_status,
                # )

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

    def get_list_of_connectors_to_run(self):

        GenericConnector.config_object = ConfigReader.read_config(
            GenericConnector.config_file
        )

        config_connector_classnames_list = Tools.get_classnames(
            GenericConnector.config_object
        ).items()

        connector_classnames_list = config_connector_classnames_list

        # args_connector_classnames_list = self.filter_varargs(
        #     Tools.filter_in_list,
        #     config_connector_classnames_list,
        #     True,
        #     #args.connectors,
        #     ['Allegro'],
        # )
        #
        # connector_classnames_list = self.filter_varargs(
        #     Tools.filter_disabled,
        #     args_connector_classnames_list,
        #     False,
        #     GenericConnector.config_object,
        #     self.logger,
        # )

        filtered_list = self.filter_varargs(
            Tools.filter_disabled,
            config_connector_classnames_list,
            False,
            GenericConnector.config_object,
            self.logger,
        )

        partial = connector_classnames_list > filtered_list

        connectors = [
            Tools.load_connector(
                connectorname=connector[1],
                config=GenericConnector.config_object
            )(
                name=connector[0],
                limit_books=0   # args.limit_books
            )
            for connector in connector_classnames_list
        ]

        return connectors, partial

    @staticmethod
    def filter_varargs(fun, iterable, expected, *args, **kwargs):
        return [
            item for item in iterable
            if fun(item, *args, **kwargs) == expected
        ]
