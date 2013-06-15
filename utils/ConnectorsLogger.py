import logging
import logging.handlers
#from utils import MultiLevelConfigParser
import utils
import os
import sys
from datetime import datetime

def logger_instance(config, force_logger_in_tests=False):
    return ConnectorsLogger.logger_instance(config, force_logger_in_tests)

class ConnectorsLogger(object):

    _loggers = {}
    handler_classes = {'FILE':logging.FileHandler,
                       'SMTP':logging.handlers.SMTPHandler,
                       'CONSOLE':logging.StreamHandler,
                       'SYSLOG':logging.handlers.SysLogHandler}

    severities = {'DEBUG':logging.DEBUG,
              'INFO':logging.INFO,
              'WARNING':logging.WARNING,
              'ERROR':logging.ERROR,
              'CRITICAL':logging.CRITICAL
              }

    '''
    Known limitations of ConnectorsLogger.logger_instance() method
    We remeber single instance of logger for each config file, not for each logger name (as logggin.getLogger does)
    It possible that 2 files configure one logger instance (if logger name in 2 config files are the same.
    In that case logger will be configured twice, and only second config will be valid.

    It is strongly recommended to use one logger instance name only in one config file across whole project.
    To make sure logger config is as expected, reload_config(config_file) should be executed.
    '''
    @staticmethod
    def logger_instance(config_file=None, force_logger_in_tests=False):
        #a little bit 'hacky' way of telling logger not to run in tests
        if sys.argv[0] == '/usr/bin/nosetests' and not force_logger_in_tests:
            logger = logging.getLogger('null_logger')
            logger.handlers = []
            logger.addHandler(logging.NullHandler())
            return logger

        if not config_file:
            try:
                return ConnectorsLogger._loggers['']
            except KeyError:
                return ConnectorsLogger()
        elif not os.path.exists(config_file):
             raise IOError('Log config file %s, does not exist' % config_file)
        else:
            try:
                return ConnectorsLogger._loggers[config_file]
            except KeyError:
                return ConnectorsLogger(config_file)


    def config_formatter(self, config):
        if not config:
            return None
        format = config.get('format', None)
        if not format:
            return None
        date_format = config.get('date_format', None)
        try:
             return logging.Formatter(fmt=format, datefmt=date_format)
        except:
            self.logger.warning('Could not format logging', exc_info=True)
            return None

    def config_severity_handlers(self, severity):
        config = dict(self.config.items(severity, vars={'date':datetime.now().strftime('%Y%m%d%H%M%S')}))
        handlers_list = config.get('log_handlers', '')
        if handlers_list:
            handlers = handlers_list.split(',')
            for handler in handlers:
                if handler == 'FILE':
                    log_file = config.get('file', 'log/connectors.log')
                    log_dir = os.path.dirname(log_file)
                    if log_dir and not os.path.exists(log_dir):
                        os.makedirs(log_dir)
                    handler_object = self.handler_classes[handler](log_file, mode='a')

                elif handler == 'SMTP':
                    mailhost = config['mailhost']
                    fromaddr = config['fromaddr']
                    toaddrs = config['toaddrs'].split(',')
                    subject = config.get('subject', 'Error Executing Connectors')

                    credentials = config.get('credentials', None)

                    #backward compatibility (python < 2.6)
                    (minor, major) = sys.version_info[0:2]
                    if minor <= 2 and major < 6:
                        credentials = None

                    if credentials:
                        credentials = tuple(credentials.split(','))
                        handler_object = self.handler_classes[handler](mailhost, fromaddr, toaddrs, subject, credentials)
                    else:
                        handler_object = self.handler_classes[handler](mailhost, fromaddr, toaddrs, subject)
                elif handler == 'SYSLOG':
                    handler_object = self.handler_classes[handler]('/dev/log')
                else:
                    handler_object = self.handler_classes[handler]()
                handler_object.setLevel(self.severities[severity])
                formatter = self.config_formatter(config)
                if formatter:
                    handler_object.setFormatter(formatter)
                self.logger.addHandler(handler_object)

    def set_handlers(self):
        if not self.logger:
            return
        #clean up handlers each time logger config is read
        self.logger.handlers = []

        if self.config:
            for severity in self.severities.keys():
                if severity in self.config.sections():
                    self.config_severity_handlers(severity)
        else:
            handler_object = logging.StreamHandler()
            handler_object.setLevel(logging.DEBUG)
            self.logger.addHandler(handler_object)

    def reload_config(self, log_config):
        if not log_config:
            self.logger_name = 'connectors'
            self.level = 'DEBUG'
            self.log_config = ''
            self.config = None
        elif not os.path.exists(log_config):
                raise IOError('Log config file %s, does not exist' % self.log_config)
        else:
            self.log_config = log_config
            self.config = utils.MultiLevelConfigParser({'level':'DEBUG', 'logger':'connectors'})
            self.config.read(self.log_config)
            self.level = self.config.get('DEFAULT', 'level')
            self.logger_name = self.config.get('DEFAULT', 'logger')

        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.severities[self.level])
        self.set_handlers()

    def __init__(self, log_config=''):
        if log_config in self._loggers:
            raise Exception('Dont even try to run GenericConnector constructor\nUse logger_instance instead\n')
        else:
            self._loggers[log_config] = self
        self.reload_config(log_config)

    def debug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)

    def exception(self, *args, **kwargs):
        self.logger.exception(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self.logger.critical(*args, **kwargs)
