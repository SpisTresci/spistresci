import nose
from nose.tools import *
from utils import NoseUtils

from xml.etree import ElementTree as et
from connectors.specific import Nexto
from connectors.specific import eClicto
from connectors.specific import CzeskieKlimaty
import os

class TestSpecificConnectors():

    def setUp(self):
        Nexto.config_file = 'unittests/data/specific_connectors/conf/test.ini'
        eClicto.config_file = 'unittests/data/specific_connectors/conf/test.ini'
        CzeskieKlimaty.config_file = 'unittests/data/specific_connectors/conf/test.ini'

    def tearDown(self):
        pass

    def test_nexto_make_dict_1(self):
        nexto = Nexto()

        dicts = os.path.join('unittests/data/specific_connectors/dict/nexto_formated_1.dict')
        xml = os.path.join('unittests/data/specific_connectors/xml/nexto_formated_1.xml')

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

    def test_eclicto_make_dict_1(self):
        eclicto = eClicto()

        dicts = os.path.join('unittests/data/specific_connectors/dict/eclicto_formated_1.dict')
        xml = os.path.join('unittests/data/specific_connectors/xml/eclicto_formated_1.xml')

        f = open(dicts, 'r')
        root = et.parse(xml).getroot()

        lines = f.readlines()
        offers = list(root[0])

        eq_(len(lines), 1)
        eq_(len(offers), 1)

        for line, offer in zip(lines, offers):
            eq_(eval(line), eclicto.makeDict(offer))

    def test_eclicto_make_dict_100(self):
        eclicto = eClicto()

        dicts = os.path.join('unittests/data/specific_connectors/dict/eclicto_formated_100.dict')
        xml = os.path.join('unittests/data/specific_connectors/xml/eclicto_formated_100.xml')

        f = open(dicts, 'r')
        root = et.parse(xml).getroot()

        lines = f.readlines()
        offers = list(root[0])

        eq_(len(lines), 100)
        eq_(len(offers), 100)

        for line, offer in zip(lines, offers):
            eq_(eval(line), eclicto.makeDict(offer))


    def test_czeskieklimaty_make_dict_1(self):
        czeskieklimaty = CzeskieKlimaty()

        dicts = os.path.join('unittests/data/specific_connectors/dict/czeskieklimaty_formated_1.dict')
        xml = os.path.join('unittests/data/specific_connectors/xml/czeskieklimaty_formated_1.xml')

        f = open(dicts, 'r')
        root = et.parse(xml).getroot()

        lines = f.readlines()
        offers = list(root[0])

        eq_(len(lines), 1)
        eq_(len(offers), 1)

        for line, offer in zip(lines, offers):
            eq_(eval(line), czeskieklimaty.makeDict(offer))

    def test_czeskieklimaty_make_dict_100(self):
        czeskieklimaty = CzeskieKlimaty()

        dicts = os.path.join('unittests/data/specific_connectors/dict/czeskieklimaty_formated_100.dict')
        xml = os.path.join('unittests/data/specific_connectors/xml/czeskieklimaty_formated_100.xml')

        f = open(dicts, 'r')
        root = et.parse(xml).getroot()

        lines = f.readlines()
        offers = list(root[0])

        eq_(len(lines), 100)
        eq_(len(offers), 100)

        for line, offer in zip(lines, offers):
            eq_(eval(line), czeskieklimaty.makeDict(offer))


