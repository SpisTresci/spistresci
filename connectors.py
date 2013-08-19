#!/usr/bin/python
import ConfigParser
import sys
import os

from utils import logger_instance, filter_varargs
from connectors import Tools
from connectors.generic import *
from sqlwrapper import *
from datetime import datetime
from final import Final

def run_connectors(connector):
    connector.createSession()

    connector.fetchData()
    connector.applyFilters()

    connector.parse()

    f = Final()
    f.insert(connector)
    connector.closeSession()

def run_reference_connectors(connector):
    connector.fetchData()
    connector.applyFilters()
    connector.parse()

def run_backup(connector):
    #only download, do not unpack
    connector.fetchData(unpack=False)

def choose_your_destiny(app_name):
    return getattr(sys.modules[__name__], 'run_%s' % app_name)


def run_load_backup(connector):
    import glob
    connector.backup_dir = os.path.join("backup", connector.name.lower())
    for archive in glob.glob(os.path.join(connector.backup_dir, "*")):
        connector.fetched_files = []
        connector.decompress_backup_dir(archive, connector.backup_archive)

        connector.applyFilters()
        connector.createSession()
        connector.parse()
        connector.closeSession()

def main():

    base_name = os.path.basename(sys.argv[0])
    app_name = os.path.splitext(base_name)[0]
    conf_name = '%s.ini' % app_name
    GenericConnector.config_file = os.path.join('conf', conf_name)
    GenericConnector.read_config()
    Logger = logger_instance(GenericConnector.config_object.get('DEFAULT', 'log_config'))

    #this is dict.items()
    connector_classnames_list = Tools.get_classnames(GenericConnector.config_object).items()
    connector_classnames_list = filter_varargs(Tools.filter_in_list, connector_classnames_list, True, sys.argv[1:])
    connector_classnames_list = filter_varargs(Tools.filter_disabled, connector_classnames_list, False, GenericConnector.config_object, Logger)

    if app_name != 'backup':
        SqlWrapper.init(GenericConnector.config_object.get('DEFAULT', 'db_config'), connectors=[con[0] for con in connector_classnames_list])
    connectors = [ Tools.load_connector(connectorname=connector[1], config=GenericConnector.config_object)
                   #insert any connector constructor parameters here
                   (name=connector[0])
                   for connector in connector_classnames_list ]

    Logger.debug('Created folowing connectors %s' % [connector.name for connector in connectors])

    us = UpdateStatus()

    us.start = datetime.now()
    us.manual = True
    us.partial = len(connector_classnames_list) > 0

    fail = False
    for connector in connectors:
        try:
            uss = UpdateStatusService(us, connector)
            choose_your_destiny(app_name)(connector)
            uss.success = True
        except Exception:
            fail = True
            Logger.exception('Error executing %s, in connector %s' % (app_name, connector.name))

    us.end = datetime.now()
    if not fail:
        us.success = True
    us.finished = True

    us.session.commit()
    us.session.close()

    Logger.debug('Execution finished')

if __name__ == '__main__':
    main()
