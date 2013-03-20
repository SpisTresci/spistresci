import nose
from nose.tools import *

from generic import GenericConnector, GenericBase
from utils import NoseUtils

from datetime import datetime
import os
import shutil
import tempfile
import hashlib


class MockConnector(GenericConnector):
    pass

class TestGenericConnector():
    
    def setUp(self):
        MockConnector.config_file = 'unittests/data/generic_connector/conf/test.ini'
        self.mc = MockConnector()

    def tearDown(self):
        if os.path.exists(self.mc.backup_dir):
            shutil.rmtree(self.mc.backup_dir)
        if os.path.exists(self.mc.unpack_dir):
            shutil.rmtree(self.mc.unpack_dir)
     
    def test_init(self):
        ok_(self.mc is not None)
        eq_(self.mc.url, 'http://www.google.com/images/srpr/logo3w.png')
        ok_(type(self.mc.config) is dict, 'config should be dict')
        eq_(self.mc.filename,'generic.xml')
            #check with one minute accuracy
        now = datetime.now().strftime('%Y%m%d%H%M')
        pattern='unittests/data/generic_connector/backup/'+now
        eq_(pattern,self.mc.backup_dir[:-3])
        eq_(self.mc.backup_archive, self.mc.ArchiveType.UNCOMPRESSED)
        eq_(self.mc.mode, self.mc.BookList_Mode.SINGLE_XML)

    def test_download_no_args(self):
        self.mc.downloadFile()
        filename = os.path.join(self.mc.backup_dir, self.mc.filename)
        ok_(os.path.exists(filename),'File %s should exist'%filename)

    def test_download_specified_filename(self):
        filename = 'test.xml'
        self.mc.downloadFile(filename = filename)
        filepath = os.path.join(self.mc.backup_dir, filename)
        ok_(os.path.exists(filepath),'File %s should exist'%filepath)

    def test_download_specified_url(self):
        url = 'http://i.s-microsoft.com/global/ImageStore/PublishingImages/logos/hp/logo-lg-1x.png'
        self.mc.downloadFile(url = url)
        filename = os.path.join(self.mc.backup_dir, self.mc.filename)
        ok_(os.path.exists(filename),'File %s should exist'%filename)

    #e.g. wiki requires non-bot user-agent
    def test_download_with_specified_headers(self):
        url = 'http://upload.wikimedia.org/wikipedia/en/b/bc/Wiki.png'
        headers = {'User-Agent':'I am not a bot'}
        self.mc.downloadFile(url = url, headers = headers)
        filename = os.path.join(self.mc.backup_dir, self.mc.filename)
        ok_(os.path.exists(filename),'File %s should exist'%filename)


    @nottest
    def _unpack_set_up(self, filename):
        self.filename = filename
        self.path = 'unittests/data/generic_connector/archives'
        self.mc.unpack_dir = '/tmp/unittests/unpack_dir'

    def assertUnpack(self, sample_file, sample_md5):
        if sample_file and sample_md5:
            ok_(os.path.exists(sample_file))
            ok_(os.path.exists(sample_md5))
            f = open(sample_md5)
            md5sum = f.read().split(' ')[0]
            f.close()
            f = open(sample_file)
            text = f.read()
            f.close()
            f_sum = hashlib.md5(text)
            eq_(md5sum,f_sum.hexdigest())
    
    def test_unpack_zip(self):
        self._unpack_set_up('sample.zip')
        self.mc.unpackZIP(os.path.join(self.path, self.filename))
        sample_file = os.path.join(self.mc.unpack_dir, 'sample')
        sample_md5 =os.path.join(self.mc.unpack_dir, 'sample.md5')
        self.assertUnpack(sample_file, sample_md5)

    def test_unpack_gzip(self):
        self._unpack_set_up('sample.gz')
        self.mc.unpackGZIP(os.path.join(self.path, self.filename))
        sample_file = os.path.join(self.mc.unpack_dir, 'sample')
        sample_md5 =os.path.join(self.path, 'sample.md5')
        self.assertUnpack(sample_file, sample_md5)

    def test_unpack_with_unpack_file_set(self):
        self.mc.unpack_file = 'sample'
        self.test_unpack_gzip()
   

    @NoseUtils.skip
    def test_validateISBN(self):
        pass

    @NoseUtils.skipIf(True, 'Not implemented yet')
    def test_validatePrice(self):
        pass

    @NoseUtils.skipIf(True)
    def test_validateSize(self):
        pass
    @NoseUtils.skipBecause('Not implemented yet')
    def test_validateAuthors(self):
        pass
            
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

