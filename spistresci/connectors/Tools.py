from utils.compatibility import OrderedDict
import ConfigParser

def get_classnames(config):
    connector_classnames = OrderedDict()
    for connector in config.sections():
        connector_name = None
        try:
            connector_name =config.get(connector, 'classname')
        except ConfigParser.NoOptionError:
            pass
        finally:
            if not connector_name:
                connector_name = connector
            connector_classnames[connector] = connector_name
    return connector_classnames

def filter_in_list(connector_classname, filter_list, logger=None):
    return not filter_list or connector_classname[0] in filter_list

def filter_disabled(connector_classname, config, logger=None):
    try:
        disabled = config.getboolean(connector_classname[0], 'disabled')
        if disabled and logger:
            logger.info('Connector %s disabled in configuration' % connector_classname[0])
        return disabled
    except ConfigParser.NoOptionError:
        return False

''' Class decorator to prevent applaying filters on decorated connector'''
def notFilterableConnector(org_class):
    old_applySingleFilter = getattr(org_class, 'applySingleFilter', None)

    def applySingleFilter(self, *args, **kwargs):
        raise NotImplementedError('One Does Not Simply apply filter on %s without implementation' % org_class.__name__ )

    org_class.applySingleFilter = applySingleFilter
    return org_class


def load_class(modulename, classname):
    modulename=str(modulename)
    classname=str(classname)
    module =  __import__(modulename, globals(), locals(), [classname])
    return getattr(module, classname)

def load_connector(connectorname, config=None, modulename='spistresci.connectors.specific'):
    if config:
        try:
            modulename = config.get(connectorname, 'connector_module')
        except ConfigParser.NoOptionError:
            pass
    return load_class(modulename, connectorname)
 
def load_filter(filterstring):
    '''
    'a.b.c.d' -> load_class('a.b.c','d')
    'd' -> load_class('filters','d')
    '''
    splited = filterstring.split('.')
    module = splited[:-1] 
    module = '.'.join(module) or 'filters'
    filtername = splited[-1]
    return load_class(module, filtername)

