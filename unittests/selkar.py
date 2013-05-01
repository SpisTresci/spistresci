from utils import NoseUtils
from nose.tools import *
from db_base import BaseDBTestFixture
from connectors.specific import Selkar
'''
Note:
Running this test standalone may cause following exception:
Exception AttributeError: "'NoneType' object has no attribute 'path'" in <bound method BezKartek.__del__ of <bezkartek.BezKartek.BezKartek object at 0xXXXXXX>> ignored

This is caused by "os" module beeing unloaded before executing BezKartek.__del__()
It's related to python bug http://bugs.python.org/issue5099
and generally it's not very risky, so screw it.
'''

class TestSelkar(BaseDBTestFixture):
    config_file = 'unittests/data/selkar/conf/test.ini'
    connector_class = Selkar

    @raises(NotImplementedError)
    def test_cant_apply_filters(self):
        self.connector.filters = 'a,b,c'
        self.connector.applyFilters()

    def test_do_nothing(self):
        pass
