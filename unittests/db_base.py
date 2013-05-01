from sqlalchemy.orm import sessionmaker
from connectors.generic import GenericConnector
from sqlwrapper import SqlWrapper
from nose.tools import *
#FIXME:
'''
Running this test standalone may cause following exception:
Exception AttributeError: "'NoneType' object has no attribute 'path'" in <bound method BezKartek.__del__ of <bezkartek.BezKartek.BezKartek object at 0xXXXXXX>> ignored

This is caused by "os" module beeing unloaded before executing BezKartek.__del__()
It's related to python bug http://bugs.python.org/issue5099
and generally it's not very risky, so screw it.
'''

class BaseDBTestFixture():

    @classmethod
    def setUpClass(cls):
        cls.connectors = [cls.connector_class.class_name()]
        GenericConnector.config_file = cls.config_file
        cls.connector = cls.connector_class()
        SqlWrapper.init(config_file=cls.connector.config_object.get('DEFAULT', 'db_config'), connectors=cls.connectors, auto_write_to_db=False)
        cls.engine = SqlWrapper.getEngine()

        cls.Session = sessionmaker(bind=cls.engine, autoflush=False)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.connection = self.engine.connect()
        self.session = self.Session(bind=self.connection)

        #FIXME:
        #There is some strange issue with creating/deleting triggers on sqlite, 
        #that causes tests to fail with
        #(OperationalError) no such trigger: <Connector>BookPriceOnInsert
        #or
        #(OperationalError) trigger <Connector>BookPriceOnInsert already exists
        #therefore this has to be temporarly disabled.
        #SqlWrapper.createTriggers()
        SqlWrapper.createTables()

    def tearDown(self):
        self.session.rollback()
        self.session.close()
        self.connection.close()
        SqlWrapper.getBaseClass().metadata.drop_all()

    def test_tables_created(self):
        eq_(self.engine.name, 'sqlite')
        eq_(self.engine.table_names(),
        ['%s%s' % (self.connector_class.class_name(), table) for table in 'Author', 'Book', 'BookDescription', 'BookPrice', 'BooksAuthors'])

#        eq_(self.connection.info, {})


    def test_do_nothing(self):
        pass
