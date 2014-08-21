import os
import nose
from nose.tools import *

from utils import MultiLevelConfigParser
from ConfigParser import SafeConfigParser
from utils.compatibility import OrderedDict


class TestMultiLevelConfigNoUTF(object):

    def readFromParser(self, configs):
        return self.cp.read(configs)
    
    def assertDefaultOption(self, option, expected_value):
        try:
            eq_(self.cp.get('DEFAULT',option), expected_value)
        except:
            eq_(None, expected_value)

    def assertOption(self, option, section, expected_value):
        try:
            eq_(self.cp.get(section, option), expected_value)
        except:
            eq_(None, expected_value)

    def assertSections(self, sections):
        eq_(self.cp.sections(), sections)
        

    def setUp(self):
        self.org_conf_levels = MultiLevelConfigParser.config_levels
        self.cp = MultiLevelConfigParser()
        self.config_file='unittests/data/multilevel_config_parser/conf/test_base.ini'
        self.config_basename = os.path.basename(self.config_file)

    def tearDown(self):
        MultiLevelConfigParser.config_levels = self.org_conf_levels

    def test_default_behaviour(self):
        self.cp = SafeConfigParser()
        eq_([self.config_file], self.cp.read(self.config_file))
        self.assertSections(['section0', 'section1'])

        for opt in range(5):
            self.assertDefaultOption('default_opt%d'%(opt), 'test_base')

        for ses in self.cp.sections():
            for opt in range(5):
                self.assertOption('%s_opt%d'%(ses, opt), ses, 'test_base')

    def test_read_read_from_multiple_files_same_as_default(self):
        self.config_file = [self.config_file, 'unittests/data/multilevel_config_parser/conf/test_base.first.ini']
        eq_(self.config_file, self.readFromParser(self.config_file))
        self.assertSections(['section0', 'section1'])

        for opt in range(5):
            self.assertDefaultOption('default_opt%d'%(opt), 'test_base.first')
            self.assertOption('section0_opt%d'% opt, 'section0', 'test_base.first')
            self.assertOption('section1_opt%d'% opt, 'section1', 'test_base')

    def test_multilevel_config_basic_read(self):
        os.environ['st_environment'] = 'first'
        os.environ['st_host'] = 'second'
        eq_(self.readFromParser(self.config_file), ['unittests/data/multilevel_config_parser/conf/test_base%sini'%x for x in '.','.first.','.first.second.'])
        self.assertSections(['section0', 'section1'])
        for opt in range(5):
            self.assertDefaultOption('default_opt%d'%(opt), 'test_base.first.second')
            self.assertOption('section0_opt%d'%(opt), 'section0', 'test_base.first.second')
            self.assertOption('section1_opt%d'%(opt), 'section1', 'test_base')

    def test_multilevel_config_with_levels_set(self):
        MultiLevelConfigParser.config_levels = OrderedDict([('first','first'),('second','second')])
        eq_(self.readFromParser(self.config_file), ['unittests/data/multilevel_config_parser/conf/test_base%sini'%x for x in '.','.first.','.first.second.'])
        self.assertSections(['section0', 'section1'])
        for opt in range(5):
            self.assertDefaultOption('default_opt%d'%(opt), 'test_base.first.second')
            self.assertOption('section0_opt%d'%(opt), 'section0', 'test_base.first.second')
            self.assertOption('section1_opt%d'%(opt), 'section1', 'test_base')
     
    def test_multilevel_config_with_set_config_levels(self):
        self.cp.set_config_levels(OrderedDict([('first','first'),('second','second')]))
        eq_(self.readFromParser(self.config_file), ['unittests/data/multilevel_config_parser/conf/test_base%sini'%x for x in '.','.first.','.first.second.'])
        self.assertSections(['section0', 'section1'])
        for opt in range(5):
            self.assertDefaultOption('default_opt%d'%(opt), 'test_base.first.second')
            self.assertOption('section0_opt%d'%(opt), 'section0', 'test_base.first.second')
            self.assertOption('section1_opt%d'%(opt), 'section1', 'test_base')

    def test_multilevel_config_with_levels_set_twice(self):
        self.cp.set_config_levels(OrderedDict([('first','first'),('second','second')]))
        MultiLevelConfigParser.config_levels = OrderedDict([('first','first')])
        #overriding class config_levels doesnt change already defined instances field config_levels
        eq_(self.readFromParser(self.config_file), ['unittests/data/multilevel_config_parser/conf/test_base%sini'%x for x in '.','.first.','.first.second.'])
        self.assertSections(['section0', 'section1'])
        for opt in range(5):
            self.assertDefaultOption('default_opt%d'%(opt), 'test_base.first.second')
            self.assertOption('section0_opt%d'%(opt), 'section0', 'test_base.first.second')
            self.assertOption('section1_opt%d'%(opt), 'section1', 'test_base')


        #hovewer changes the value for newly created instances
        self.cp = MultiLevelConfigParser()
        eq_(self.readFromParser(self.config_file), ['unittests/data/multilevel_config_parser/conf/test_base%sini'%x for x in '.','.first.'])
        self.assertSections(['section0', 'section1'])
        for opt in range(5):
            self.assertDefaultOption('default_opt%d'%(opt), 'test_base.first')
            self.assertOption('section0_opt%d'%(opt), 'section0', 'test_base.first')
            self.assertOption('section1_opt%d'%(opt), 'section1', 'test_base')

    def test_multilevel_config_with_3_levels_set(self):
        MultiLevelConfigParser.config_levels = OrderedDict([('first','first'),('second','second'),('other','third')])
        eq_(self.readFromParser(self.config_file), ['unittests/data/multilevel_config_parser/conf/test_base%sini'%x for x in '.','.first.','.first.second.','.first.second.third.'])
        self.assertSections(['section0', 'section1'])
        for opt in range(5):
            self.assertDefaultOption('default_opt%d'%(opt), 'test_base.first.second.third')
            self.assertOption('section0_opt%d'%(opt), 'section0', 'test_base.first.second.third')
            self.assertOption('section1_opt%d'%(opt), 'section1', 'test_base')

    def test_multilevel_config_with_section_partly_overriden(self):
        MultiLevelConfigParser.config_levels = OrderedDict([('sth','4th')])
        eq_(self.readFromParser(self.config_file), ['unittests/data/multilevel_config_parser/conf/test_base%sini'%x for x in '.','.4th.'])
        self.assertSections(['section0', 'section1','section2'])
        for opt in range(4):
            self.assertDefaultOption('default_opt%d'%(opt), 'test_base.4th')
            self.assertOption('section0_opt%d'%(opt), 'section0', 'test_base.4th')
            self.assertOption('section1_opt%d'%(opt), 'section1', 'test_base')
            self.assertOption('section2_opt%d'%(opt), 'section2', 'test_base.4th')

        self.assertDefaultOption('default_opt4', 'test_base')
        self.assertOption('section0_opt4', 'section0', 'test_base')
        self.assertOption('section1_opt4', 'section1', 'test_base')
        self.assertOption('section2_opt4', 'section2', None)


 
class TestMultiLevelConfigUTF(TestMultiLevelConfigNoUTF):
    def readFromParser(self, configs):
        return self.cp.read(configs, force_utf=True)
