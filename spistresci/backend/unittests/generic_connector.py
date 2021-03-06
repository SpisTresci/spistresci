import nose
from nose.tools import *

from connectors.generic import GenericConnector, GenericBase
from utils import NoseUtils
from utils import ConfigReader
from datetime import datetime
import os
import shutil
import tempfile
import hashlib
import ConfigParser

        
class MockConnector(GenericConnector):
    pass

class TestGenericConnector(object):

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
        eq_(self.mc.filename, 'generic.xml')
            #check with one minute accuracy
        now = datetime.now().strftime('%Y%m%d%H%M')
        pattern = 'unittests/data/generic_connector/backup/' + now
        eq_(pattern, self.mc.backup_dir[:-3])
        eq_(self.mc.backup_archive, self.mc.ArchiveType.UNCOMPRESSED)
        eq_(self.mc.mode, self.mc.BookList_Mode.SINGLE_XML)
    
    @NoseUtils.skipIf(not NoseUtils.network_available_for_tests(), 'Network connection broken')
    def test_download_no_args(self):
        self.mc.downloadFile()
        filename = os.path.join(self.mc.backup_dir, self.mc.filename)
        ok_(os.path.exists(filename), 'File %s should exist' % filename)

    @NoseUtils.skipIf(not NoseUtils.network_available_for_tests(), 'Network connection broken')
    def test_download_specified_filename(self):
        filename = 'test.xml'
        self.mc.downloadFile(filename=filename)
        filepath = os.path.join(self.mc.backup_dir, filename)
        ok_(os.path.exists(filepath), 'File %s should exist' % filepath)

    @NoseUtils.skipIf(not NoseUtils.network_available_for_tests(), 'Network connection broken')
    def test_download_specified_url(self):
        url = 'http://i.s-microsoft.com/global/ImageStore/PublishingImages/logos/hp/logo-lg-1x.png'
        self.mc.downloadFile(url=url)
        filename = os.path.join(self.mc.backup_dir, self.mc.filename)
        ok_(os.path.exists(filename), 'File %s should exist' % filename)

    #e.g. wiki requires non-bot user-agent
    @NoseUtils.skipIf(not NoseUtils.network_available_for_tests(), 'Network connection broken')
    def test_download_with_specified_headers(self):
        url = 'http://upload.wikimedia.org/wikipedia/en/b/bc/Wiki.png'
        headers = {'User-Agent':'I am not a bot'}
        self.mc.downloadFile(url=url, headers=headers)
        filename = os.path.join(self.mc.backup_dir, self.mc.filename)
        ok_(os.path.exists(filename), 'File %s should exist' % filename)


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
            eq_(md5sum, f_sum.hexdigest())

    def test_unpack_zip(self):
        self._unpack_set_up('sample.zip')
        self.mc.unpackZIP(os.path.join(self.path, self.filename))
        sample_file = os.path.join(self.mc.unpack_dir, 'sample')
        sample_md5 = os.path.join(self.mc.unpack_dir, 'sample.md5')
        self.assertUnpack(sample_file, sample_md5)

    def test_unpack_gzip(self):
        self._unpack_set_up('sample.gz')
        self.mc.unpackGZIP(os.path.join(self.path, self.filename))
        sample_file = os.path.join(self.mc.unpack_dir, 'sample')
        sample_md5 = os.path.join(self.path, 'sample.md5')
        self.assertUnpack(sample_file, sample_md5)

    def test_unpack_with_unpack_file_set(self):
        self.mc.unpack_file = 'sample'
        self.test_unpack_gzip()


class TestGenericConnectorWithGenericConfigFileField(TestGenericConnector):
    def setUp(self):
        GenericConnector.config_file = 'unittests/data/generic_connector/conf/test.ini'
        self.mc = MockConnector()


class TestGenericConnectorWithMockupReadConfigExecuted(TestGenericConnector):
    def setUp(self):
        MockConnector.config_file = 'unittests/data/generic_connector/conf/test.ini'
        MockConnector.config_object = ConfigReader.read_config(MockConnector.config_file)
        self.mc = MockConnector()

class TestGenericConnectorWithGenericReadConfigExecuted(TestGenericConnector):
    def setUp(self):
        MockConnector.config_file = 'unittests/data/generic_connector/conf/test.ini'
        MockConnector.config_object = ConfigReader.read_config(MockConnector.config_file)
        self.mc = MockConnector()

class TestExceptionIfRemovingParrentDir(object):
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
        ok_(not os.path.exists(_dir), '%s dir %s shoud be removed' % (_type, _dir))

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


class TestParseConfig(object):
    def setUp(self):
        MockConnector.config_file = 'unittests/data/generic_connector/conf/test_parse_config.ini'
        self.mc = MockConnector()

    @raises(ConfigParser.NoSectionError)
    def test_raises_no_section_error(self):
        class NotDefinedConnector(GenericConnector):
            pass
        NotDefinedConnector.config_file = self.mc.config_file
        NotDefinedConnector()

    @NoseUtils.skipBecause('T183: Passing name of file to parse_config currently does not work')
    @raises(ConfigParser.Error)
    def test_wrong_config_file(self):
        self.mc.parse_config('NOT_A_FILE')
        eq_(self.mc.config_file, 'NOT_A_FILE')


    def test_standard_section(self):
        self.mc = MockConnector('StandardSection')
        for i in [1,2,3]:
            eq_(self.mc.config['option'+str(i)],'val'+str(i))

    def test_dotted_section(self):
        self.mc = MockConnector('DottedSection')
        eq_(self.mc.config['option1'],
        {'test1':'val1.test1', 
        'test2':{'':'val1.test2','test3':'val1.test2.test3'}, 
        '':'val1'})

class TestCreatePPUrl(object):
    def setUp(self):
        MockConnector.config_file = 'unittests/data/generic_connector/conf/test.ini'
        self.mc = MockConnector()
        self.book = {'test_key': 'testvalue'}

    def test_correct_config(self):
        eq_(self.mc.pp_url, {'' : 'this_is_%(test_key)s_%(partner_id)s', 
                            'partner_id' : 'partner_id', 
                            'test_key' : {'pattern':'(test)', 'replace':'\\1_replace_'}})

    def test_run_standard_config(self):
        self.mc.create_pp_url(self.book)
        eq_(self.book['pp_url'], 'this_is_test_replace_value_partner_id')

    def test_run_empty_config(self):
        book_copy= self.book.copy()
        self.mc.pp_url = None
        self.mc.create_pp_url(book_copy)
        eq_(book_copy, self.book)
    
    def test_run_no_replace_patterns(self):
        del self.mc.pp_url['test_key']
        self.mc.create_pp_url(self.book)
        eq_(self.book['pp_url'], 'this_is_testvalue_partner_id')


    def test_run_more_keys_in_config(self):
        self.mc.pp_url['other_key'] = {'pattern':'dummy', 'replace':'dummy'}
        self.mc.create_pp_url(self.book)
        eq_(self.book['pp_url'], 'this_is_test_replace_value_partner_id')

class TestFulfillRequirements(object):
    def setUp(self):
        MockConnector.config_file = 'unittests/data/generic_connector/conf/test.ini'
        self.mc = MockConnector()
     
    def test_correct_config(self):
        eq_(self.mc.fulfill,  {'condition': 'dummy && dummy1', 'search': {'dummy': 'dummy_regex', 'dummy1': 'dummy_regex1'}})
    
    def test_no_requirements_defined(self):
        self.mc.fulfill = None
        ok_(self.mc.fulfillRequirements({}))
        ok_(self.mc.fulfillRequirements({'not_empty':'book'}))

    @raises(KeyError)
    def test_exception_on_empty_book(self):
        self.mc.fulfill = {'condition': 'condition', 'search': {'search': '^regex'}}
        ok_(self.mc.fulfillRequirements({}))

    @raises(KeyError)
    def test_exception_on_wrong_search(self):
        self.mc.fulfill = {'condition': 'condition', 'search': {'not_existing_key': '^regex'}}
        ok_(self.mc.fulfillRequirements({'some_key':'some_value'}))

    @raises(SyntaxError)
    def test_exception_on_wrong_condition(self):
        self.mc.fulfill = {'condition': 'condition that will not evaluate', 'search': {'some_key': '^some_value'}}
        ok_(self.mc.fulfillRequirements({'some_key':'some_value'}))

    def test_single_condition(self):
        self.mc.fulfill = {'condition': 'search', 'search': {'search': '^regex'}}
        ok_(self.mc.fulfillRequirements({'search': 'regex11', 'other': 'dummy'}))

    def test_and_condition(self):
        self.mc.fulfill = {'condition': 'search & other', 'search': {'search': '^regex', 'other': '^dummy'}}
        ok_(self.mc.fulfillRequirements({'search': 'regex11', 'other': 'dummy'}))

    def test_or_condition(self):
        self.mc.fulfill = {'condition': 'search | other', 'search': {'search': '^regex', 'other': '^dummy'}}
        ok_(self.mc.fulfillRequirements({'search': 'regex11', 'other': 'sth_else'}))

    def test_or_and_condition(self):
        self.mc.fulfill = {'condition': 'search | other & search', 'search': {'search': '^regex', 'other': '^dummy'}}
        ok_(self.mc.fulfillRequirements({'search': 'regex11', 'other': 'sth_else'}))

    def test_not_searched_condition(self):
        self.mc.fulfill = {'condition': 'search', 'search': {'search': '^regex'}}
        ok_(not self.mc.fulfillRequirements({'search': 'r11', 'other': 'dummy'}))

    def test_not_searched_and_condition(self):
        self.mc.fulfill = {'condition': 'search & other', 'search': {'search': '^regex', 'other': '^dummy'}}
        ok_(not self.mc.fulfillRequirements({'search': 'regex11', 'other': 'not_dummy'}))
