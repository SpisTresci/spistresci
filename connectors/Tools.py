from utils import logger_instance
import ConfigParser

def get_classnames(config):
    connector_classnames = {}
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

def filter_classnames(connector_classnames, filter_list, logger=None):
    if not connector_classnames:
        return []
    elif not filter_list:
        return connector_classnames

    names_from_filter = []
    for name in filter_list:
        if name in connector_classnames.keys():
            names_from_filter.append(name)
        elif logger:
            logger.debug('Connector %s not known'%name)

    final_connector_list = {}
    for cn in names_from_filter:
        final_connector_list[cn] = connector_classnames[cn]
    return final_connector_list

def load_class(modulename, classname):
    modulename=str(modulename)
    classname=str(classname)
    module =  __import__(modulename, globals(), locals(), [classname])
    return getattr(module, classname)

def load_connector(connectorname, config=None, modulename='connectors.specific'):
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

