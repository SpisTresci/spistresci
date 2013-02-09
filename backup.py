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

    for connector in connectors:
        try:
            #only download, do not unpack
            connector.fetchData(unpack=False)
        except Exception:
            Logger.exception('Error in backup, connector %s'%connector.name)
    Logger.debug('Backup execution finished')

if __name__ == '__main__':
    main()
