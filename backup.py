#!/usr/bin/python
import ConfigParser
import sys

from connectors import *
from connectors_logger import logger_instance

def main():
    GenericConnector.config_file = 'conf/backup.ini'
    GenericConnector.read_config()
    Logger = logger_instance(GenericConnector.config_object.get('DEFAULT','log_config'))

    connectors = [ getattr(sys.modules[__name__],connector)()
                  for connector in GenericConnector.config_object.sections() ]

    Logger.debug('Created folowing connectors %s'%[connector.name for connector in connectors])

    try:
        for connector in connectors:
            connector.downloadFile()
    except Exception as e:
        Logger.exception('Error executing backup')
    else:
        Logger.debug('Backup execution finished')


if __name__ == '__main__':
    main()
