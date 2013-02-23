from generic import GenericConnector
from connectors_logger import logger_instance
import ConfigParser

def get_classnames():
    connector_classnames = {}
    for connector in GenericConnector.config_object.sections():
        connector_name = None
        try:
            connector_name = GenericConnector.config_object.get(connector, 'classname')
        except ConfigParser.NoOptionError:
            pass
        finally:
            if not connector_name:
                connector_name = connector
            connector_classnames[connector]=connector_name
    return connector_classnames

def filter_classnames(connector_classnames, filter_list):
    if not connector_classnames:
        return []
    elif not filter_list:
        return connector_classnames

    names_from_filter = []
    for name in filter_list:
        if name in connector_classnames.keys():
            names_from_filter.append(name)
        else:
            Logger = logger_instance(GenericConnector.config_object.get('DEFAULT', 'log_config'))
            Logger.debug('Connector %s not known for config file %s' %(name, GenericConnector.config_file))

    final_connector_list = {} 
    for cn in names_from_filter:
        final_connector_list[cn] = connector_classnames[cn]
    return final_connector_list
