import nose
from nose.tools import *
from utils import NoseUtils
from connectors import Tools
import lxml.etree as et
from connectors.generic import GenericConnector
from connectors.specific import *
import os
import glob
import re
import sys
class TestSpecificConnectors():

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @nottest
    def _test_dict(self, connector, xml, dicts, assert_lines):
        f = open(dicts, 'r')
        root = connector.get_et().parse(xml).getroot()

        lines = f.readlines()
        offers = connector.weHaveToGoDeeper(root, connector.depth)
        if connector.skip_offers:
            offers = offers[connector.skip_offers:]

        eq_(len(lines), assert_lines)
        eq_(len(offers), assert_lines)

        for line, offer in zip(lines, offers):
            evaluated_dict = eval(line)
            fresh_dict = connector.makeDict(offer)

            evaluated_dict_keys = evaluated_dict.keys()
            fresh_dict_keys = fresh_dict.keys()

            evaluated_dict_keys.sort()
            fresh_dict_keys.sort()

            eq_(evaluated_dict_keys, fresh_dict_keys)

            for key, key2 in zip(evaluated_dict_keys, fresh_dict_keys):
                eq_(evaluated_dict[key], fresh_dict[key2])

    def test_connectors(self):
    	self.inputpath='unittests/data/specific_connectors/'
        GenericConnector.config_file = os.path.join(self.inputpath, 'conf/test.ini')
        GenericConnector.read_config()

        connector_classnames = Tools.get_classnames(GenericConnector.config_object)
        connectors = [ Tools.load_connector(connectorname=connector[1], config=GenericConnector.config_object)(name=connector[0]) for connector in connector_classnames .items() ]

    	for connector in connectors:
            for x in glob.glob(os.path.join(self.inputpath, 'dict', '%s_formated_*.dict'%connector.name.lower())):
                pattern = re.compile('.*?(\d*)\.dict$')
                num = pattern.match(x).group(1)
                if num.isdigit():
                    yield self._test_dict, connector, x.replace('dict', 'xml'), x, int(num)

            yield self._test_depricated_xml_tags_dict, connector
            yield self._test_depricated_columns, connector
            yield self._test_unique_columns, connector

    @nottest
    def _test_depricated_xml_tags_dict(self, connector):
        depricated_xml_tags = ['isbn', 'format']

        for key in connector.xml_tag_dict.keys():
            for tag in depricated_xml_tags:
                assert connector.xml_tag_dict[key][0] != tag, "%s != %s, connector: %s" % (connector.xml_tag_dict[key][0], tag, connector.name)

    @nottest
    def _test_depricated_columns(self, connector):
        depricated_columns = ['isbn', 'format']

        Book = connector.getConcretizedClass(connector, "Book")

        for column in Book.__table__.columns:
            for depricated_column_name in depricated_columns:
                assert column.name != depricated_column_name, "%s != %s, connector: %s" % (column.name, depricated_column_name, connector.name)

    def _test_unique_columns(self, connector):
        unique_columns = ['external_id']
        Book = connector.getConcretizedClass(connector, "Book")

        for unique_column in unique_columns:
            for c in Book.__table__.columns:
                if c.name == unique_column:
                    ok_(c.unique)
