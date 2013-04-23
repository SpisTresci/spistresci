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

    def weHaveToGoDeeper(self, root, depth):
        for i in range(int(depth)):
            root=root[0]
        return root

    @nottest
    def _test_dict(self, connector, xml, dicts, assert_lines):
        f = open(dicts, 'r')
        root = et.parse(xml).getroot()

        lines = f.readlines()
        offers = self.weHaveToGoDeeper(root, connector.config.get('depth',0))
        skip_offers = connector.config.get('skip_offers',0)
        if skip_offers:
            offers = offers[int(skip_offers):]

        eq_(len(lines), assert_lines)
        eq_(len(offers), assert_lines)

        for line, offer in zip(lines, offers):
            eq_(eval(line), connector.makeDict(offer))

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

