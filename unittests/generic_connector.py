import nose
from nose.tools import *
from generic import GenericConnector

import os
import shutil
import tempfile
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

class TestExceptionIfRemovingParrentDir():
    def setUp(self):
        MockConnector.config_file = 'unittests/data/generic_connector/conf/test.ini'
        self.mc = MockConnector()
        self.mc.backup_dir = tempfile.mkdtemp()
        self.mc.unpack_dir = tempfile.mkdtemp()
        self.cwd = os.getcwd()
        
    def tearDown(self):
        os.chdir(self.cwd)
        if os.path.exists(self.mc.backup_dir):
            shutil.rmtree(self.mc.backup_dir)
        if os.path.exists(self.mc.unpack_dir):
            shutil.rmtree(self.mc.unpack_dir)
    
    @nottest
    def _test_rm(self, _dir, _type):
        ok_(os.path.exists(_dir))
        self.mc._rm_ifpossible(_dir, _type)
        ok_(not os.path.exists(_dir), '%s dir %s shoud be removed'% (_type, _dir) )

    def test_correct_rm_backup(self):
        self._test_rm(self.mc.backup_dir, 'backup')

    def test_correct_rm_unpack(self):
        self._test_rm(self.mc.unpack_dir, 'unpack')
    
    @raises(IOError)
    def test_fail_rm_backup(self):
        new_cwd = os.path.join(self.mc.backup_dir, 'cwd')
        os.makedirs(new_cwd)
        os.chdir(new_cwd)
        self._test_rm(self.mc.backup_dir, 'backup')
    
    @raises(IOError)
    def test_fail_rm_unpack(self):
        new_cwd = os.path.join(self.mc.unpack_dir, 'cwd')
        os.makedirs(new_cwd)
        os.chdir(new_cwd)
        self._test_rm(self.mc.unpack_dir, 'unpack')

