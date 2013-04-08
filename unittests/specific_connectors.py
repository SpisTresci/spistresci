import nose
from nose.tools import *
from utils import NoseUtils

from xml.etree import ElementTree as et
from connectors.specific import Nexto
import os

class TestSpecificConnectors():

    def setUp(self):
        Nexto.config_file = 'unittests/data/specific_connectors/conf/test.ini'

    def tearDown(self):
        pass

    def test_nexto_make_dict(self):
        nexto = Nexto()

        dicts = os.path.join('unittests/data/specific_connectors/dict/nexto_formated.dict')
        xml = os.path.join('unittests/data/specific_connectors/xml/nexto_formated.xml')

        f = open(dicts, 'r')
        root = et.parse(xml).getroot()

        lines = f.readlines()
        offers = list(root)

        eq_(len(lines), 1)
        eq_(len(offers), 1)

        for line, offer in zip(lines, offers):
            eq_(eval(line), nexto.makeDict(offer))



    def test_nexto_make_dict_100(self):
        nexto = Nexto()

        dicts = os.path.join('unittests/data/specific_connectors/dict/nexto_formated_100.dict')
        xml = os.path.join('unittests/data/specific_connectors/xml/nexto_formated_100.xml')

        f = open(dicts, 'r')
        root = et.parse(xml).getroot()

        lines = f.readlines()
        offers = list(root)

        eq_(len(lines), 100)
        eq_(len(offers), 100)

        for line, offer in zip(lines, offers):
            eq_(eval(line), nexto.makeDict(offer))
