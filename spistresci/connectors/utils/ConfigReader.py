import ConfigParser
from spistresci.connectors.utils.MultiLevelConfigParser import MultiLevelConfigParser


class ConfigReader(object):

    @classmethod
    def read_config(cls, config_file):
        config_object = MultiLevelConfigParser()
        #TODO: our config should be case sensitive, somehow this does not work
        #config_object.optionxfrom = str
        if not config_object.read(config_file, force_utf=True):
            raise ConfigParser.Error('Could not read config from file %s' % config_file)

        return config_object

    @classmethod
    def _get_conf_option(cls, _list, value, dic):
        key = _list[0]
        _list = _list[1:]
        old_value = {}
        if type(dic) is dict:
            old_value = dic.get(key, {})
        if not type(old_value) is dict:
            old_value = {'':old_value}
        if _list:
            old_value[_list[0]] = ConfigReader._get_conf_option(_list, value, old_value)
        else:
            old_value[''] = value
        if old_value.keys() == ['']:
            old_value = old_value['']
        return old_value

    @classmethod
    def parse_config(cls, config_file=None, section=None, config_object=None, vars={}):

        if not config_object:
            config_object = ConfigReader.read_config(config_file)

        config = {}
        for item in config_object.items(section, vars = vars):
            #this is for managaging config options like
            #option.suboption = 11
            (key, value) = item
            splited = key.split('.')
            config[splited[0]] = ConfigReader._get_conf_option(splited, value, config)

        return config