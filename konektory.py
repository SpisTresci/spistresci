#!/usr/bin/python
import ConfigParser
import sys

from connectors_logger import logger_instance
from connectors import *

def main():

    GenericConnector.config_file = 'conf/database_tests.ini'
    GenericConnector.read_config()
    Logger = logger_instance(GenericConnector.config_object.get('DEFAULT','log_config'))

    connector_classnames = {}
    for connector in GenericConnector.config_object.sections():
        connector_name = None
        try:
            connector_name = GenericConnector.config_object.get(connector,'classname')
        except ConfigParser.NoOptionError:
            pass
        finally:
            if not connector_name:
                connector_name = connector
            connector_classnames[connector]=connector_name

    connectors = [ getattr(sys.modules[__name__],connector[1])(name=connector[0])
                  for connector in connector_classnames.items() ]

    Logger.debug('Created folowing connectors %s'%[connector.name for connector in connectors])

    for connector in connectors:
        try:
            connector.fetchData()
            connector.parse()
        except Exception:
            Logger.exception('Error executing connector %s'%connector.name)
    Logger.debug('Execution finished')


if __name__ == '__main__':
    main()
