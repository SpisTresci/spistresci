import nose
from nose.tools import *
from nose.plugins.capture import Capture

from utils.ConnectorsLogger import logger_instance

from StringIO import StringIO
import sys
import os
import logging

MockStderr = StringIO()

''' 
All tests in this file inherit from TestGenericLogger, so all of them has test_log and test_ml_exist.
It means that for each test these 2 tests will be executed 
and in most cases the only thing to do is to set config_path and expected result
'''
class TestGenericLogger(object):
    config_file = None
    config_path = 'unittests/data/logger/conf'
    expected = 'test_debug\ntest_info\ntest_warning\ntest_error\ntest_critical\n'
    stderr = []

    def __init__(self):
        pass

    def setUp(self):
        MockStderr.truncate(0)
        if self.config_file:
            config_file = os.path.join(self.config_path, self.config_file)
        else:
            config_file = None
        self.ml = logger_instance(config_file, force_logger_in_tests=True)
        self.ml.debug('test_debug')
        self.ml.info('test_info')
        self.ml.warning('test_warning')
        self.ml.error('test_error')
        self.ml.critical('test_critical')

    @classmethod
    def setUpClass(cls):
        cls.stderr.append(sys.stderr)
        MockStderr.truncate(0)
        sys.stderr = MockStderr

    @classmethod
    def tearDownClass(cls):
        sys.stderr = cls.stderr.pop()

    def tearDown(self):
        pass

    def test_ml_exist(self):
        ok_(self.ml is not None)

    def test_log(self):
        eq_(MockStderr.getvalue(), self.expected)

class TestCriticalConsole(TestGenericLogger):
    config_file = 'test_critical_console.ini'
    expected = 'test_critical\n'

class TestErrorConsole(TestGenericLogger):
    config_file = 'test_error_console.ini'
    expected = 'test_error\ntest_critical\n'

class TestWarningConsole(TestGenericLogger):
    config_file = 'test_warning_console.ini'
    expected = 'test_warning\ntest_error\ntest_critical\n'

class TestInfoConsole(TestGenericLogger):
    config_file = 'test_info_console.ini'
    expected = 'test_info\ntest_warning\ntest_error\ntest_critical\n'

class TestDebugConsole(TestGenericLogger):
    config_file = 'test_debug_console.ini'

    def test_empty_test(self):
        pass

    def test_additional_test(self):
        self.test_log()

class TestDebugConsoleMissingSections(TestGenericLogger):
    config_file = 'test_debug_console_missing_section.ini'


class TestDebugConsoleErrorFile(TestGenericLogger):
    config_file = 'test_debug_console_error_file.ini'
    file_name = '/tmp/log_error.log'
    expected_file_content = 'test_error\ntest_critical\n'

    def test_log_file(self):
        ok_(os.path.exists(self.file_name))#,'File %s should exist'%self.file_name)
        f = open(self.file_name, 'rU')
        eq_(f.read(), self.expected_file_content)
        f.close()

    def tearDown(self):
        TestGenericLogger.tearDown(self)
        if os.path.exists(self.file_name):
            f = open(self.file_name, 'w')
            f.truncate()
            f.close()

    @classmethod
    def tearDownClass(cls):
        TestGenericLogger.tearDownClass()
        if os.path.exists(cls.file_name):
            os.remove(cls.file_name)
'''
This tests checks if you can set several handlers on several levels, when each handler has different formatting
In that case all handlers are CONSOLE handlers, so we read from stdout output of every handler.
E.G for critical level log message there will be 4 entries in output, each one differently formatted
'''
class TestFormats(TestGenericLogger):
    config_file = 'test_formats.ini'
    expected = 'DEBUGtest_debug\nINFOtest_info\nWARNINGtest_warning\ntest_format test_warning\nERRORtest_error\ntest_format test_error\nother_format test_error\nCRITICALtest_critical\ntest_format test_critical\nCRITICALCRITICAL test_critical\nother_format test_critical\n'

class TestReloadConfig(TestGenericLogger):
    config_file = 'test_debug_console.ini'
    def setUp(self):
        MockStderr.truncate(0)
        config_file = os.path.join(self.config_path, self.config_file)
        self.ml = logger_instance(config_file, force_logger_in_tests=True)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='this should not be in stderr after reload')
        handler.setFormatter(formatter)
        self.ml.logger.addHandler(handler)

        self.ml.reload_config(config_file)
        self.ml.debug('test_debug')
        self.ml.info('test_info')
        self.ml.warning('test_warning')
        self.ml.error('test_error')
        self.ml.critical('test_critical')

class TestSingleInstance(TestCriticalConsole):
    config_file = 'test_single_instance.ini'
    def setUp(self):
        MockStderr.truncate(0)
        #log to ml logger
        TestCriticalConsole.setUp(self)
        #configure ml2 logger
        config_file = os.path.join(self.config_path, self.config_file)
        self.ml2 = logger_instance(config_file, force_logger_in_tests=True)

    def test_single_instance(self):
        #log to ml2 logger
        self.ml2.debug('ml2_debug')
        self.ml2.info('ml2_info')
        self.ml2.warning('ml2_warning')
        self.ml2.error('ml2_error')
        self.ml2.critical('ml2_critical')
        #log to ml logger which in fact is ml2 logger
        self.ml.debug('ml_debug')
        self.ml.info('ml_info')
        self.ml.warning('ml_warning')
        self.ml.error('ml_error')
        self.ml.critical('ml_critical')
        self.expected = self.expected + 'ml2_critical\nml_critical\n'
        self.test_log()

class TestSingletonException(TestGenericLogger):
    expected = ''

    def setUp(self):
        MockStderr.truncate(0)
        if self.config_file:
            config_file = os.path.join(self.config_path, self.config_file)
        else:
            config_file = None
        self.ml = logger_instance(config_file, force_logger_in_tests=True)

    @raises(Exception)
    def test_singleton_exception_for_empty_config(self):
        from utils import ConnectorsLogger
        self.ml2 = ConnectorsLogger.ConnectorsLogger()

    @raises(Exception)
    def test_singleton_exception_for_config(self):
        config_file = os.path.join(self.config_path, 'test_debug_console.ini')
        from utils import ConnectorsLogger
        self.ml2 = ConnectorsLogger.ConnectorsLogger()
        self.ml3 = ConnectorsLogger.ConnectorsLogger()
