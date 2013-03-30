#!/usr/bin/python
import ConfigParser
import sys
import os

from utils import logger_instance
from connectors import Tools
from connectors.generic import *
from sqlwrapper import *


def run_connectors(connector):
    connector.fetchData()
    connector.applyFilters()
    connector.parse()

def run_backup(connector):
    #only download, do not unpack
    connector.fetchData(unpack=False)

def choose_your_destiny(app_name):
    return getattr(sys.modules[__name__], 'run_%s' % app_name)

def main():

    base_name = os.path.basename(sys.argv[0])
    app_name = os.path.splitext(base_name)[0]
    conf_name  = '%s.ini' % app_name
    GenericConnector.config_file = os.path.join('conf', conf_name)
    GenericConnector.read_config()
    Logger = logger_instance(GenericConnector.config_object.get('DEFAULT', 'log_config'))

    connector_classnames = Tools.get_classnames()
    final_connector_dic = Tools.filter_classnames(connector_classnames, sys.argv[1:])

    if app_name != 'backup':
        SqlWrapper.init(GenericConnector.config_object.get('DEFAULT', 'db_config'), connectors=final_connector_dic.keys())
    connectors = [ Tools.load_connector(classname=connector[1], config=GenericConnector.config_object)
                   (name=connector[0])
                   for connector in final_connector_dic.items() ]

    Logger.debug('Created folowing connectors %s' % [connector.name for connector in connectors])

    for connector in connectors:
        try:
            choose_your_destiny(app_name)(connector)
        except Exception:
            Logger.exception('Error executing %s, in connector %s' % (app_name, connector.name) )
    Logger.debug('Execution finished')

if __name__ == '__main__':
    main()
