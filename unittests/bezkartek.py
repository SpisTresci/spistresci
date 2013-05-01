from utils import NoseUtils
from nose.tools import *
from db_base import BaseDBTestFixture
from connectors.specific import BezKartek

'''
Note:
Running this test standalone may cause following exception:
Exception AttributeError: "'NoneType' object has no attribute 'path'" in <bound method BezKartek.__del__ of <bezkartek.BezKartek.BezKartek object at 0xXXXXXX>> ignored

This is caused by "os" module beeing unloaded before executing BezKartek.__del__()
It's related to python bug http://bugs.python.org/issue5099
and generally it's not very risky, so screw it.
'''

class TestBezKartek(BaseDBTestFixture):
    config_file = 'unittests/data/bezkartek/conf/test.ini'
    connector_class = BezKartek


    def test_do_nothing_bezkartek(self):
        pass
