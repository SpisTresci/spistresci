import nose
from nose.tools import *
from utils import NoseUtils
from connectors import Tools
from xml.etree import ElementTree as et
from connectors.generic import GenericConnector
from connectors.specific import *
import os

class TestSpecificConnectors():

    def set_params(self, connector):
        connector.shortdicts = os.path.join(self.inputpath, 'dict/%s_formated_%s.dict' % (connector.name.lower(), connector.config['short']))
        connector.xmlshort = os.path.join(self.inputpath, 'xml/%s_formated_%s.xml' % (connector.name.lower(), connector.config['short']))
        connector.xmllong = os.path.join(self.inputpath, 'xml/%s_formated_%s.xml' % (connector.name.lower(), connector.config['long']))
        connector.longdicts = os.path.join(self.inputpath, 'dict/%s_formated_%s.dict' % (connector.name.lower(), connector.config['long']))

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
        offers = self.weHaveToGoDeeper(root, connector.config['depth'])

        eq_(len(lines), assert_lines)
        eq_(len(offers), assert_lines)

        for line, offer in zip(lines, offers):
            eq_(eval(line), connector.makeDict(offer))

    @nottest
    def test_make_dict_short(self, connector):
        self._test_dict(connector, connector.xmlshort, connector.shortdicts, int(connector.config['short']))

    @nottest
    def test_make_dict_long(self, connector):
        self._test_dict(connector, connector.xmllong, connector.longdicts, int(connector.config['long']))

    def test_connectors(self):
    	self.inputpath='unittests/data/specific_connectors/'
	GenericConnector.config_file = os.path.join(self.inputpath, 'conf/test.ini')
        GenericConnector.read_config()

        connector_classnames = Tools.get_classnames(GenericConnector.config_object)
	connectors = [ Tools.load_connector(connectorname=connector[1], config=GenericConnector.config_object)(name=connector[0]) for connector in connector_classnames .items() ]

    	for connector in connectors:
	    self.set_params(connector)        
            yield self.test_make_dict_short, connector
            yield self.test_make_dict_long, connector

