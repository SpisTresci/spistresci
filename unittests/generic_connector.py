import nose
from nose.tools import *
from generic import GenericConnector

import re
from datetime import datetime


class MockConnector(GenericConnector):
   pass 

class TestGenericConnector():
    
    def setUp(self):
        MockConnector.config_file = 'unittests/data/generic_connector/conf/test.ini'
        self.mc = MockConnector()
     
    def test_init(self):
        ok_(self.mc is not None)
        eq_(self.mc.url,'localhost://')
        ok_(type(self.mc.config) is dict,'config should be dict')
        eq_(self.mc.filename,'generic.xml')
        #check with one minute accuracy
        now = datetime.now().strftime('%Y%m%d%H%M')
        pattern='unittests/data/generic_connector/backup/'+now
        eq_(pattern,self.mc.backup_dir[:-3])
        eq_(self.mc.backup_archive,0)


class TestGenericConnectorWithGenericConfigFileField(TestGenericConnector):
    def setUp(self):
        GenericConnector.config_file = 'unittests/data/generic_connector/conf/test.ini'
        self.mc = MockConnector() 


class TestGenericConnectorWithMockupReadConfigExecuted(TestGenericConnector):
    def setUp(self):
        MockConnector.config_file = 'unittests/data/generic_connector/conf/test.ini'
        MockConnector.read_config()
        self.mc = MockConnector()

class TestGenericConnectorWithGenericReadConfigExecuted(TestGenericConnector):
    def setUp(self):
        MockConnector.config_file = 'unittests/data/generic_connector/conf/test.ini'
        GenericConnector.read_config()
        self.mc = MockConnector()
