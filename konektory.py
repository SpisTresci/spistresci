#!/usr/bin/python
import ConfigParser
import sys

from connectors_logger import logger_instance
from connectors import *
from connectors import Tools

def main():

    GenericConnector.read_config()
    Logger = logger_instance(GenericConnector.config_object.get('DEFAULT', 'log_config'))

    connector_classnames = Tools.get_classnames()
    final_connector_dic = Tools.filter_classnames(connector_classnames, sys.argv[1:])

    connectors = [ getattr(sys.modules[__name__],connector[1])(name=connector[0])
                  for connector in final_connector_dic.items() ]

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
