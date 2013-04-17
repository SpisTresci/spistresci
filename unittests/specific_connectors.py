import nose
from nose.tools import *
from utils import NoseUtils

from xml.etree import ElementTree as et
from connectors.generic import GenericConnector
from connectors.specific import *
import os

class TestSpecificConnectors():

    inputpath='unittests/data/specific_connectors/'
    GenericConnector.config_file = os.path.join(inputpath, 'conf/test.ini')

    def setUp(self):
        self.shortdicts = os.path.join(self.inputpath, 'dict/%s_formated_%d.dict' % (self.connector.name.lower(), self.short))
        self.xmlshort = os.path.join(self.inputpath, 'xml/%s_formated_%d.xml' % (self.connector.name.lower(), self.short))
        self.xmllong = os.path.join(self.inputpath, 'xml/%s_formated_%d.xml' % (self.connector.name.lower(), self.long))
        self.longdicts = os.path.join(self.inputpath, 'dict/%s_formated_%d.dict' % (self.connector.name.lower(), self.long))
        self.offers_from_root=lambda x:list(x[0])

    def tearDown(self):
        pass


class Assertions():

    @nottest
    def _test_dict(self, xml, dicts, assert_lines):
        f = open(dicts, 'r')
        root = et.parse(xml).getroot()

        lines = f.readlines()
        offers = self.offers_from_root(root)

        eq_(len(lines), assert_lines)
        eq_(len(offers), assert_lines)

        for line, offer in zip(lines, offers):
            eq_(eval(line), self.connector.makeDict(offer))

    def test_make_dict_short(self):
        self._test_dict(self.xmlshort, self.shortdicts, self.short)        

    def test_make_dict_long(self):
        self._test_dict(self.xmllong, self.longdicts, self.long)        


class TestNexto(TestSpecificConnectors, Assertions):
    def setUp(self):
        self.short=1
        self.long=100
        self.connector = Nexto()
        TestSpecificConnectors.setUp(self)
        self.offers_from_root=lambda x:list(x)

class TestEclicto(TestSpecificConnectors, Assertions):
    def setUp(self):
        self.short=1
        self.long=100
        self.connector = eClicto()
        TestSpecificConnectors.setUp(self)

class TestCzeskieKlimaty(TestSpecificConnectors, Assertions):
    def setUp(self):
        self.short=1
        self.long=100
        self.connector = CzeskieKlimaty()
        TestSpecificConnectors.setUp(self)

class TestWolneEbooki(TestSpecificConnectors, Assertions):
    def setUp(self):
        self.short=1
        self.long=19
        self.connector = WolneEbooki()
        TestSpecificConnectors.setUp(self)
        self.offers_from_root=lambda x:list(x)

class TestBezKartek(TestSpecificConnectors, Assertions):
    def setUp(self):
        self.short=1
        self.long=100
        self.connector = BezKartek()
        TestSpecificConnectors.setUp(self)

class TestDobryEbook(TestSpecificConnectors, Assertions):
    def setUp(self):
        self.short=1
        self.long=65
        self.connector = DobryEbook()
        TestSpecificConnectors.setUp(self)
        self.offers_from_root=lambda x:list(x)

class TestEmpik(TestSpecificConnectors, Assertions):
    def setUp(self):
        self.short=1
        self.long=100
        self.connector = Empik()
        TestSpecificConnectors.setUp(self)
        self.offers_from_root=lambda x:list(x)

class TestTaniaKsiazka(TestSpecificConnectors, Assertions):
    def setUp(self):
        self.short=1
        self.long=100
        self.connector = TaniaKsiazka()
        TestSpecificConnectors.setUp(self)
        self.offers_from_root=lambda x:list(x)

class TestKoobe(TestSpecificConnectors, Assertions):
    def setUp(self):
        self.short=1
        self.long=100
        self.connector = Koobe()
        TestSpecificConnectors.setUp(self)

class TestWoblink(TestSpecificConnectors, Assertions):
    def setUp(self):
        self.short=1
        self.long=100
        self.connector = Woblink()
        TestSpecificConnectors.setUp(self)

class TestBooksOn(TestSpecificConnectors, Assertions):
    def setUp(self):
        self.short=1
        self.long=6
        self.connector = BooksOn()
        TestSpecificConnectors.setUp(self)


class TestRW2010(TestSpecificConnectors, Assertions):
    def setUp(self):
        self.short=1
        self.long=100
        if NoseUtils.network_available_for_tests():
            self.connector = RW2010()
            TestSpecificConnectors.setUp(self)
        else:
            self.connector = None
        self.offers_from_root=lambda x:list(x)

    @NoseUtils.skipIf(not NoseUtils.network_available_for_tests(), 'Network connection broken')
    def test_make_dict_short(self):
        Assertions.test_make_dict_short(self)

    @NoseUtils.skipIf(not NoseUtils.network_available_for_tests(), 'Network connection broken')
    def test_make_dict_long(self):
        Assertions.test_make_dict_long(self)
