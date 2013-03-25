from generic import GenericConnector
from connectors import Selkar
from sql_wrapper import SqlWrapper
from utils import NoseUtils

from sqlalchemy.pool import NullPool
from nose.tools import *

'''
Note:
Running this test standalone may cause following exception:
Exception AttributeError: "'NoneType' object has no attribute 'path'" in <bound method BezKartek.__del__ of <bezkartek.BezKartek.BezKartek object at 0xXXXXXX>> ignored

This is caused by "os" module beeing unloaded before executing BezKartek.__del__()
It's related to python bug http://bugs.python.org/issue5099
and generally it's not very risky, so screw it.
'''

class TestSelkar():
    @classmethod
    def setUpClass(cls):
        GenericConnector.config_file = 'unittests/data/selkar/conf/test.ini'
        cls.sk = Selkar()
        SqlWrapper.init(Selkar.config_object.get('DEFAULT', 'db_config'), ['Selkar'])
        cls.engine = SqlWrapper.getEngine()

    @classmethod
    def tearDownClass(cls):
        pass
       
    def setUp(self):
        self.connection = self.engine.connect()

    def tearDown(self):
        self.connection.close()

    @NoseUtils.skipBecause('Problems with sqlite inmemory sessions')
    def test_engine_init(self):
        eq_(self.engine.name,'sqlite')
        eq_(self.engine.table_names(), ['SelkarAuthor', 'SelkarBook', 'SelkarBookDescription', 'SelkarBookPrice', 'SelkarBooksAuthors'])
        eq_(self.connection.info, {})

    @raises(NotImplementedError)
    def test_cant_apply_filters(self):
        self.sk.filters='a,b,c'
        self.sk.applyFilters()
