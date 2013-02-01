#!/usr/bin/python
import ConfigParser
import sys

from connectors_logger import logger_instance
from connectors import *

def main():

    GenericConnector.read_config()
    Logger = logger_instance(GenericConnector.config_object.get('DEFAULT','log_config'))

    connectors = [ getattr(sys.modules[__name__],connector)()
                  for connector in GenericConnector.config_object.sections() ]

    Logger.debug('Created folowing connectors %s'%[connector.name for connector in connectors])

    try:
        for connector in connectors:
            connector.fetchData()
            connector.parse()
    except Exception as e:
        Logger.exception('Error executing connectors')
    else:
        Logger.debug('Execution finished')


if __name__ == '__main__':
    main()
