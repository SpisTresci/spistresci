from generic import GenericConnector
from connectors import BezKartek
from sql_wrapper import SqlWrapper

from nose.tools import *

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

    def test_engine_init(self):
        eq_(self.engine.name,'sqlite')
        eq_(self.engine.table_names(), ['BezKartekAuthor', 'BezKartekBook', 'BezKartekBookDescription', 'BezKartekBookPrice', 'BezKartekBooksAuthors'])
        eq_(self.connection.info, {})


