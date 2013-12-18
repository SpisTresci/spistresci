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
from models import *
from sqlwrapper import *
from datetime import datetime
from final import Final
from utils import ConfigReader

def run_update(connector, args):
    connector.createSession()

    connector.fetchData()
    connector.applyFilters()

    connector.parse()

    Final.session = connector.session

    if args.insert:
        Final.insert(connector)

    #Final.inner_merge(connector)

    connector.closeSession()

def run_insert(connector, args):
    connector.createSession()
    Final.insert(connector)
    connector.closeSession()

def run_update_reference(connector, args):
    connector.fetchData()
    connector.applyFilters()
    connector.parse()

def run_merge(connector, args):
    connector.createSession()
    Final.session = connector.session

    from final import MiniBook
    bookstores = Final.session.query(MiniBook.bookstore).group_by(MiniBook.bookstore).all()
    bookstores = [bookstore[0] for bookstore in bookstores]

    if all(bookstore in args.connectors for bookstore in bookstores):
        connector =  None # means, that merge will be done for all connectors

    if args.by == 'isbn':
        Final.mergeByISBN(connector)
    elif args.by == 'title':
        Final.mergeByTitle(connector)

    if not connector:
        exit()

def run_backup(connector, args):
    #only download, do not unpack
    connector.fetchData(unpack=False)

#use when creating tests
def run_test_create(connector, args):
    connector.fetchData(download=False)
    connector._parse_make_test_dict()

def run_measure_length(connector):
    connector.fetchData()
    connector._parse_measure_length()

def run_load_backup(connector, args):
    connector.backup_dir = os.path.join("backup", connector.name.lower())
    for archive in glob.glob(os.path.join(connector.backup_dir, "*")):
        connector.fetched_files = []
        connector.decompress_backup_dir(archive, connector.backup_archive)

        connector.applyFilters()
        connector.createSession()
        connector.parse()
        connector.closeSession()

def update_status(args, partial):
    if args.mode not in ['backup', 'test_create', 'measure_length']: 
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
            globals()['run_%s' % args.mode](connector, args)
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
    parser.add_argument('-m', '--mode', action="store", default="update", choices=['update', 'insert', 'update-reference', 'merge', 'backup', 'load-backup', 'test-create', 'measure-length'],
                        help=   'Modes:\n\n'
                                '\tupdate               - [DEFAULT] run update for mentioned services\n'
                                '\tupdate-reference     - run update for mentioned reference services\n'
                                '\tmerge                - run proper merge algorithm according to argument <--by>\n'
                                '\tbackup               - fetch data for each of service. Do not run update.\n'
                                '\tload-backup          - load backups from backup directory.\n'
                                '\ttest-create          - create dict for unittests.\n'
                                '\tmeasure-length       - count size of.\n'
                                '\tload-services-info   - read information from services.ini\n'

                       )
    parser.add_argument('--auto', action="store_false", dest="manual", help='Should be used only by cron.')
    parser.add_argument('--no-insert', action="store_false", dest="insert", default="true", help='Argument for --mode update, which prevents insertion of books to MasterBook table.')
    parser.add_argument('--by', help='Values for --by:\n'
                                '\tisbn\n'
                                '\ttitle\n'
                        )

    parser.add_argument('connectors', action="store", nargs="*", choices=connectors + [''], default='', metavar='service_name',
                        help='Names of service to handle, positioned into list of names. Empty list means "FOR EACH".\n\n'
                             'Possible values are:\n\n' + ', '.join(connectors))
    parser.add_argument('-l', '--limit-books', type=int, default=0, 
                        help='Limit books processed for each connector. 0 (default) means process all books')
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
    GenericConnector.config_object = ConfigReader.read_config(GenericConnector.config_file)
    Logger = logger_instance(GenericConnector.config_object.get('DEFAULT', 'log_config'))

    #this is dict.items()
    config_connector_classnames_list = Tools.get_classnames(GenericConnector.config_object).items()

    args_connector_classnames_list = filter_varargs(Tools.filter_in_list, config_connector_classnames_list, True, args.connectors)
    connector_classnames_list = filter_varargs(Tools.filter_disabled, args_connector_classnames_list, False, GenericConnector.config_object, Logger)

    partial = connector_classnames_list >= filter_varargs(Tools.filter_disabled, config_connector_classnames_list, False, GenericConnector.config_object, Logger)

    if args.mode not in ['backup', 'test_create', 'measure_length']: 
        SqlWrapper.init(GenericConnector.config_object.get('DEFAULT', 'db_config'), connectors=[con[0] for con in connector_classnames_list])

    connectors = [ Tools.load_connector(connectorname=connector[1], config=GenericConnector.config_object)
                   #insert any connector constructor parameters here
                   (name=connector[0], limit_books = args.limit_books)
                   for connector in connector_classnames_list ]

    Logger.debug('Created folowing connectors %s' % [connector.name for connector in connectors])
    
    us = update_status(args, partial)
    succeed = choose_your_destiny(args, connectors, partial, Logger, us)
    close_update_status(us, succeed)

    Logger.debug('Execution finished')

if __name__ == '__main__':
    main()
