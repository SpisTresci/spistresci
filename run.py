#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import glob
import argparse
from argparse import RawTextHelpFormatter
from utils.MultiLevelConfigParser import MultiLevelConfigParser
from utils import logger_instance, filter_varargs
from connectors import Tools
from connectors.generic import *
from sqlwrapper import *
from datetime import datetime
from final import Final

def run_update(connector):
    connector.createSession()

    connector.fetchData()
    connector.applyFilters()

    connector.parse()

    f = Final()
    f.insert(connector)
    connector.closeSession()

def run_update_reference(connector):
    connector.fetchData()
    connector.applyFilters()
    connector.parse()

def run_backup(connector):
    #only download, do not unpack
    connector.fetchData(unpack=False)

def run_load_backup(connector):
    connector.backup_dir = os.path.join("backup", connector.name.lower())
    for archive in glob.glob(os.path.join(connector.backup_dir, "*")):
        connector.fetched_files = []
        connector.decompress_backup_dir(archive, connector.backup_archive)

        connector.applyFilters()
        connector.createSession()
        connector.parse()
        connector.closeSession()

def update_status(args, partial):
    if args.mode not in ['backup']:
        us = UpdateStatus()
    
        us.start = datetime.now()
        us.manual = args.manual
        us.partial = partial
        return us


def choose_your_destiny(args, connectors, partial, Logger, us):
    fail = False
    for connector in connectors:
        try:
            if us:
                uss = UpdateStatusService(us, connector)
            getattr(sys.modules[__name__], 'run_%s' % args.mode)(connector)
            if us:
                uss.success = True
        except Exception:
            fail = True
            Logger.exception('Error executing %s, in connector %s' % (args.mode, connector.name))
    return not fail

def close_update_status(us, succeed):
    if us:
        us.end = datetime.now()
        if succeed:
            us.success = True
        us.finished = True
    
        us.session.commit()
        us.session.close()

def parse_args():
    config_object = MultiLevelConfigParser()
    config_object.read('conf/update.ini', force_utf=True)

    connector_classnames_list = Tools.get_classnames(config_object).items()
    connectors = [c[0] for c in connector_classnames_list]

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-m', '--mode', action="store", default="update", choices=['update', 'update-reference', 'backup', 'load-backup'],
                        help=   'Modes:\n\n'
                                '\tupdate           - [DEFAULT] run update for mentioned services\n'
                                 '\tupdate-reference - run update for mentioned reference services\n'
                                '\tbackup           - fetch data for each of service. Do not run update.\n'
                                '\tload-backup      - load backups from backup directory.\n'

                       )
    parser.add_argument('--auto', action="store_false", dest="manual", help='Should be used only by cron.')

    parser.add_argument('connectors', action="store", nargs="*", choices=connectors + [''], default='', metavar='service_name',
                        help='Names of service to handle, positioned into list of names. Empty list means "FOR EACH".\n\n'
                             'Possible values are:\n\n' + ', '.join(connectors))
    args = parser.parse_args()

    base_name = os.path.basename(sys.argv[0])
    app_name = os.path.splitext(base_name)[0]

    if app_name != 'run':
        if app_name == 'connectors':
            args.mode = 'update'
        else:
            args.mode = app_name

    args.mode = args.mode.replace('-', '_')  # (°̯ʖ°) o_O (°͜ʖ°) ;)

    if args.connectors == '':
        args.connectors = connectors

    return args


def main():
    args = parse_args()

    GenericConnector.config_file = os.path.join('conf', '%s.ini' % args.mode)
    GenericConnector.read_config()
    Logger = logger_instance(GenericConnector.config_object.get('DEFAULT', 'log_config'))

    #this is dict.items()
    config_connector_classnames_list = Tools.get_classnames(GenericConnector.config_object).items()
    args_connector_classnames_list = filter_varargs(Tools.filter_in_list, config_connector_classnames_list, True, args.connectors)
    connector_classnames_list = filter_varargs(Tools.filter_disabled, args_connector_classnames_list, False, GenericConnector.config_object, Logger)

    partial = connector_classnames_list >= filter_varargs(Tools.filter_disabled, config_connector_classnames_list, False, GenericConnector.config_object, Logger)

    if args.mode not in ['backup']:
        SqlWrapper.init(GenericConnector.config_object.get('DEFAULT', 'db_config'), connectors=[con[0] for con in connector_classnames_list])
    connectors = [ Tools.load_connector(connectorname=connector[1], config=GenericConnector.config_object)
                   #insert any connector constructor parameters here
                   (name=connector[0])
                   for connector in connector_classnames_list ]

    Logger.debug('Created folowing connectors %s' % [connector.name for connector in connectors])
    
    us = update_status(args, partial)
    succeed = choose_your_destiny(args, connectors, partial, Logger, us)
    close_update_status(us, succeed)

    Logger.debug('Execution finished')

if __name__ == '__main__':
    main()
