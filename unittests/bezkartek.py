from generic import GenericConnector
from connectors import BezKartek
from sql_wrapper import SqlWrapper
from utils import NoseUtils
from nose.tools import *

'''
Note:
Running this test standalone may cause following exception:
Exception AttributeError: "'NoneType' object has no attribute 'path'" in <bound method BezKartek.__del__ of <bezkartek.BezKartek.BezKartek object at 0xXXXXXX>> ignored

This is caused by "os" module beeing unloaded before executing BezKartek.__del__()
It's related to python bug http://bugs.python.org/issue5099
and generally it's not very risky, so screw it.
'''

class TestBezKartek():
    @classmethod
    def setUpClass(cls):
        BezKartek.config_file = 'unittests/data/bezkartek/conf/test.ini'
        cls.bk = BezKartek()
        SqlWrapper.init(BezKartek.config_object.get('DEFAULT', 'db_config'), ['BezKartek'])
        cls.engine = SqlWrapper.getEngine()

#    def tearDownClass(self):

        
    def setUp(self):
        self.connection = self.engine.connect()

    def tearDown(self):
        self.connection.close()
    
    @NoseUtils.skipBecause('Problems with inmemory sqlite sessions')
    def test_engine_init(self):
        eq_(self.engine.name,'sqlite')
        eq_(self.engine.table_names(), ['BezKartekAuthor', 'BezKartekBook', 'BezKartekBookDescription', 'BezKartekBookPrice', 'BezKartekBooksAuthors'])
        eq_(self.connection.info, {})


