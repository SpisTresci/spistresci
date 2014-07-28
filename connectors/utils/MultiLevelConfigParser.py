import os
import socket
from ConfigParser import SafeConfigParser
from compatibility import OrderedDict
import codecs
from django.conf import settings

class MultiLevelConfigParser(SafeConfigParser):
    
    config_levels = OrderedDict([('environment','devel'),('host',socket.gethostname())])

    def set_config_levels(self, config_levels):
        self.config_levels = config_levels

    def get_multilevel_configs(self, base_config):
        config_list = [base_config]
        (name, ext) = os.path.splitext(base_config)
        for (level, default) in self.config_levels.items():
            level_value = os.environ.get('st_%s' % level,default)
            name = '%s.%s' % (name, level_value)
            config_list.append(name+ext)
        return config_list

    def _read_no_utf(self, filenames):
        if isinstance(filenames, basestring):
            config_list = self.get_multilevel_configs(filenames)
            return SafeConfigParser.read(self, config_list)
        else:
            #if list is passed as argument, then we assume programmer knows what he's doing,
            #in that case our parser behaves as default SafeConfigParser
            return SafeConfigParser.read(self, filenames)

    def read(self, filenames, force_utf=False):
        if force_utf:
            return self._read_utf(filenames)
        else:
            return self._read_no_utf(filenames)

    def _read_utf_list(self, files):
        files_read = []
        #this is compilant with _read version that does not  for multilevel
        for _file in files:
            try:
                _file = os.path.join(settings.CONNECTORS_CONFIG_DIR, _file)

                with codecs.open(_file, 'r', 'utf8') as ff:
                    self.readfp(ff)
                files_read.append(_file)
            except IOError:
                continue
        return files_read

    def _read_utf(self, filenames):
        if isinstance(filenames, basestring):
            return self._read_utf_list(self.get_multilevel_configs(filenames))
        else:
            return self._read_utf_list(filenames)

