import nose
from nose.tools import *
from utils import NoseUtils

from xml.etree import ElementTree as et
from connectors.specific import BezKartek
from connectors.specific import CzeskieKlimaty
from connectors.specific import DobryEbook
from connectors.specific import eClicto
from connectors.specific import Empik
from connectors.specific import Nexto
from connectors.specific import WolneEbooki
import os

class TestSpecificConnectors():

    def setUp(self):
        BezKartek.config_file = 'unittests/data/specific_connectors/conf/test.ini'
        CzeskieKlimaty.config_file = 'unittests/data/specific_connectors/conf/test.ini'
        DobryEbook.config_file = 'unittests/data/specific_connectors/conf/test.ini'
        eClicto.config_file = 'unittests/data/specific_connectors/conf/test.ini'
        Empik.config_file = 'unittests/data/specific_connectors/conf/test.ini'
        Nexto.config_file = 'unittests/data/specific_connectors/conf/test.ini'
        WolneEbooki.config_file = 'unittests/data/specific_connectors/conf/test.ini'

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

    def test_wolneebooki_make_dict_1(self):
        wolneebooki = WolneEbooki()

        dicts = os.path.join('unittests/data/specific_connectors/dict/wolneebooki_formated_1.dict')
        xml = os.path.join('unittests/data/specific_connectors/xml/wolneebooki_formated_1.xml')

        f = open(dicts, 'r')
        root = et.parse(xml).getroot()

        lines = f.readlines()
        offers = list(root)

        eq_(len(lines), 1)
        eq_(len(offers), 1)

        for line, offer in zip(lines, offers):
            eq_(eval(line), wolneebooki.makeDict(offer))

    def test_wolneebooki_make_dict_19(self):
        wolneebooki = WolneEbooki()

        dicts = os.path.join('unittests/data/specific_connectors/dict/wolneebooki_formated_19.dict')
        xml = os.path.join('unittests/data/specific_connectors/xml/wolneebooki_formated_19.xml')

        f = open(dicts, 'r')
        root = et.parse(xml).getroot()

        lines = f.readlines()
        offers = list(root)

        eq_(len(lines), 19)
        eq_(len(offers), 19)

        for line, offer in zip(lines, offers):
            eq_(eval(line), wolneebooki.makeDict(offer))

    def test_bezkartek_make_dict_1(self):
        bezkartek = BezKartek()

        dicts = os.path.join('unittests/data/specific_connectors/dict/bezkartek_formated_1.dict')
        xml = os.path.join('unittests/data/specific_connectors/xml/bezkartek_formated_1.xml')

        f = open(dicts, 'r')
        root = et.parse(xml).getroot()

        lines = f.readlines()
        offers = list(root[0])

        eq_(len(lines), 1)
        eq_(len(offers), 1)

        for line, offer in zip(lines, offers):
            eq_(eval(line), bezkartek.makeDict(offer))

    def test_bezkartek_make_dict_100(self):
        bezkartek = BezKartek()

        dicts = os.path.join('unittests/data/specific_connectors/dict/bezkartek_formated_100.dict')
        xml = os.path.join('unittests/data/specific_connectors/xml/bezkartek_formated_100.xml')

        f = open(dicts, 'r')
        root = et.parse(xml).getroot()

        lines = f.readlines()
        offers = list(root[0])

        eq_(len(lines), 100)
        eq_(len(offers), 100)

        for line, offer in zip(lines, offers):
            eq_(eval(line), bezkartek.makeDict(offer))

    def test_dobryebook_make_dict_1(self):
        dobryebook = DobryEbook()

        dicts = os.path.join('unittests/data/specific_connectors/dict/dobryebook_formated_1.dict')
        xml = os.path.join('unittests/data/specific_connectors/xml/dobryebook_formated_1.xml')

        f = open(dicts, 'r')
        root = et.parse(xml).getroot()

        lines = f.readlines()
        offers = list(root)

        eq_(len(lines), 1)
        eq_(len(offers), 1)

        for line, offer in zip(lines, offers):
            eq_(eval(line), dobryebook.makeDict(offer))

    def test_dobryebook_make_dict_65(self):
        dobryebook = DobryEbook()

        dicts = os.path.join('unittests/data/specific_connectors/dict/dobryebook_formated_65.dict')
        xml = os.path.join('unittests/data/specific_connectors/xml/dobryebook_formated_65.xml')

        f = open(dicts, 'r')
        root = et.parse(xml).getroot()

        lines = f.readlines()
        offers = list(root)

        eq_(len(lines), 65)
        eq_(len(offers), 65)

        for line, offer in zip(lines, offers):
            eq_(eval(line), dobryebook.makeDict(offer))

    def test_empik_make_dict_1(self):
        empik = Empik()

        dicts = os.path.join('unittests/data/specific_connectors/dict/empik_formated_1.dict')
        xml = os.path.join('unittests/data/specific_connectors/xml/empik_formated_1.xml')

        f = open(dicts, 'r')
        root = et.parse(xml).getroot()

        lines = f.readlines()
        offers = list(root)
        
	eq_(len(lines), 1)
        eq_(len(offers), 1)

        for line, offer in zip(lines, offers):
            eq_(eval(line), empik.makeDict(offer))

    def test_empik_make_dict_100(self):
        empik = Empik()

        dicts = os.path.join('unittests/data/specific_connectors/dict/empik_formated_100.dict')
        xml = os.path.join('unittests/data/specific_connectors/xml/empik_formated_100.xml')

        f = open(dicts, 'r')
        root = et.parse(xml).getroot()

        lines = f.readlines()
        offers = list(root)

        eq_(len(lines), 100)
        eq_(len(offers), 100)

        for line, offer in zip(lines, offers):
            eq_(eval(line), empik.makeDict(offer))

