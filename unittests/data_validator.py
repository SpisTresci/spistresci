# -*- coding: utf-8 -*-
import nose
from nose.tools import *
from utils import NoseUtils
from utils import DataValidator, DataValidatorError

class MockErratumLogger(object):
    def __init__(self):
        self.warned = False
        self.informed = False
        self.debug_informed = False
        self.warntext = ''
        self.infotext = ''
        self.debugtext = ''

    def warning(self, str):
        self.warned = True
        self.warntext = str

    def info(self, str):
        self.informed = True
        self.infotext = str

    def debug(self, str):
        self.debug_informed = True
        self.debugtext = str

class TestDataValidator(object):

    def setUp(self):
        self.dv = DataValidator()
        self.dv.erratum_logger = MockErratumLogger()
        self.dv.name = "TestDataValidator"

    @nottest
    def _test_validate_helper_eq(self, functionName, input, expected, *args, **kwargs):
        validateFun = getattr(self.dv, "validate" + functionName)
        validateFun(input, "id", "title", *args, **kwargs)
        eq_(input, expected)


    @nottest
    def _test_validate_helper_not_eq(self, functionName, input, expected, *args, **kwargs):
        validateFun = getattr(self.dv, "validate" + functionName)
        validateFun(input, "id", "title", *args, **kwargs)
        assert input != expected

    @nottest
    def _test_validate_helper_warning(self, functionName, input, *args, **kwargs):
        eq_(self.dv.erratum_logger.warned, False)
        validateFun = getattr(self.dv, "validate" + functionName)
        validateFun(input, "id", "title", *args, **kwargs)
        eq_(self.dv.erratum_logger.warned, True)
        self.dv.erratum_logger.warned = False
        eq_(self.dv.erratum_logger.warned, False)

    @nottest
    def _test_validate_helper_info(self, functionName, input, *args, **kwargs):
        eq_(self.dv.erratum_logger.informed, False)
        validateFun = getattr(self.dv, "validate" + functionName)
        validateFun(input, "id", "title", *args, **kwargs)
        eq_(self.dv.erratum_logger.informed, True)
        self.dv.erratum_logger.informed = False
        eq_(self.dv.erratum_logger.informed, False)

    @nottest
    @raises(Exception)
    def _test_validate_helper_raises(self, functionName, input,  *args, **kwargs):
        validateFun = getattr(self.dv, "validate" + functionName)
        validateFun(input, "id", "title", *args, **kwargs)

    def test_validate_price(self):
        yield self._test_validate_helper_eq, "Price", {}, {"price":"0"}
        yield self._test_validate_helper_eq, 'Price', {}, {'price': '-1'}, 'price', -1
        #TODO: consider what should happen id tag is empty, currently it is replaved by defalt_price
        yield self._test_validate_helper_eq, 'Price', {"price":''}, {'price':'-1'}, 'price', -1
        yield self._test_validate_helper_eq, "Price", {"price":""}, {"price":"0"}
        yield self._test_validate_helper_eq, "Price", {"price":"10"}, {"price":"1000"}
        yield self._test_validate_helper_eq, "Price", {"price":"124"}, {"price":"12400"}
        yield self._test_validate_helper_eq, "Price", {"price":"000"}, {"price":"0"}
        yield self._test_validate_helper_eq, "Price", {"price":"0"}, {"price":"0"}

        yield self._test_validate_helper_eq, "Price", {"price":"9.99"}, {"price":"999"}
        yield self._test_validate_helper_eq, "Price", {"price":"734.00"}, {"price":"73400"}
        yield self._test_validate_helper_eq, "Price", {"price":"1.00"}, {"price":"100"}
        yield self._test_validate_helper_eq, "Price", {"price":"0,17"}, {"price":"17"}
        yield self._test_validate_helper_eq, "Price", {"price":"0,09"}, {"price":"9"}
        yield self._test_validate_helper_eq, "Price", {"price":",99"}, {"price":"99"}
        yield self._test_validate_helper_eq, "Price", {"price":".00"}, {"price":"0"}

        yield self._test_validate_helper_eq, "Price", {"price":"9,99"}, {"price":"999"}
        yield self._test_validate_helper_eq, "Price", {"price":"734,00"}, {"price":"73400"}
        yield self._test_validate_helper_eq, "Price", {"price":"1,23"}, {"price":"123"}
        yield self._test_validate_helper_eq, "Price", {"price":"0,42"}, {"price":"42"}
        yield self._test_validate_helper_eq, "Price", {"price":"0,01"}, {"price":"1"}
        yield self._test_validate_helper_eq, "Price", {"price":"0.00"}, {"price":"0"}

        yield self._test_validate_helper_not_eq, "Price", {"price":"0,01"}, {"price":"001"}
        yield self._test_validate_helper_raises, 'Price', {}, 'price', 'NOT_INT'

        yield self._test_validate_helper_warning, "Price", {"price":"-5"}
        yield self._test_validate_helper_warning, "Price", {"price":"-5.57"}
        yield self._test_validate_helper_warning, "Price", {"price":"4.999"}
        yield self._test_validate_helper_warning, "Price", {"price":"4.999"}
        yield self._test_validate_helper_warning, "Price", {"price":"0,,01"}
        yield self._test_validate_helper_warning, "Price", {"price":"5,574,547"}
        yield self._test_validate_helper_warning, "Price", {"price":"5.574.547"}
        yield self._test_validate_helper_warning, "Price", {"price":"9.123456"}
        yield self._test_validate_helper_warning, "Price", {"price":"20 zl"}

    def test_validate_formats(self):
        yield self._test_validate_helper_eq, "Formats", {}, {"formats":[]}
        yield self._test_validate_helper_eq, "Formats", {"formats":""}, {"formats":[]}
        yield self._test_validate_helper_eq, "Formats", {"formats":"pdf"}, {"formats":["pdf"]}
        yield self._test_validate_helper_eq, "Formats", {"formats":"Pdf"}, {"formats":["pdf"]}
        yield self._test_validate_helper_eq, "Formats", {"formats":"PDF"}, {"formats":["pdf"]}
        yield self._test_validate_helper_eq, "Formats", {"formats":"PDF,"}, {"formats":["pdf"]}
        yield self._test_validate_helper_eq, "Formats", {"formats":"PDF,mobi"}, {"formats":["pdf", "mobi"]}
        yield self._test_validate_helper_eq, "Formats", {"formats":"PDF, mobi"}, {"formats":["pdf", "mobi"]}
        yield self._test_validate_helper_eq, "Formats", {"formats":"Pdf, Mobi"}, {"formats":["pdf", "mobi"]}
        yield self._test_validate_helper_eq, "Formats", {"formats":"Pdf, Mobi, ePub"}, {"formats":["pdf", "mobi", "epub"]}
        yield self._test_validate_helper_eq, "Formats", {"formats":"Pdf, Mobi, ePub"}, {"formats":["pdf", "mobi", "epub"]}

        yield self._test_validate_helper_eq, "Formats", {"formats":"pdf mobi epub"}, {"formats":["pdf", "mobi", "epub"]}

        yield self._test_validate_helper_eq, "Formats", {"formats":[u'pdf', u'epub', u'mobi']}, {"formats":[u"pdf", u"epub", u"mobi"]}

        yield self._test_validate_helper_warning, "Formats", {"formats":"Pdf, Mobi, Mobi"}
        yield self._test_validate_helper_warning, "Formats", {"formats":"Pdf, Mobi, MOBI"}
        yield self._test_validate_helper_warning, "Formats", {"formats":"Pdf, Mobi, PDF, MOBI"}
        yield self._test_validate_helper_warning, "Formats", {"formats":"Pdf,Mobi,PDF,MOBI"}

        yield self._test_validate_helper_warning, "Formats", {"formats":"pdf, mobi epub"}
        yield self._test_validate_helper_warning, "Formats", {"formats":"some_not_supported_format"}
        yield self._test_validate_helper_warning, "Formats", {"formats":"X,Y"}
        yield self._test_validate_helper_warning, "Formats", {"formats":"X,Y,Z"}

    def test_validate_isbns(self):
        yield self._test_validate_helper_eq, "ISBNs", {}, {"isbns":[]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":""}, {"isbns":[]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"978-83-7308-701-9"}, {"isbns":[{    "raw":"9788373087019",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '837308701X',
                                                                                                    'isbn13': '9788373087019',
                                                                                                    'core': '837308701'}]}

        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"978-83-7308-701-9"}, {"isbns":[{    "raw":"9788373087019",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '837308701X',
                                                                                                    'isbn13': '9788373087019',
                                                                                                    'core': '837308701'}]}

        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"9788373087019"}, {"isbns":[{        "raw":"9788373087019",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '837308701X',
                                                                                                    'isbn13': '9788373087019',
                                                                                                    'core': '837308701'}]}

        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"978-83-7308-701-9"}, {"isbns":[{ "raw":"9788373087019",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '837308701X',
                                                                                                    'isbn13': '9788373087019',
                                                                                                    'core': '837308701'}]}

        yield self._test_validate_helper_eq, "ISBNs", {"isbns":u"978-83-7308-701-9"}, {"isbns":[{    "raw":u"9788373087019",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '837308701X',
                                                                                                    'isbn13': '9788373087019',
                                                                                                    'core': '837308701'}]}

        yield self._test_validate_helper_eq, "ISBNs", {"isbns":u"978\u201083\u20107308\u2010701\u20109"}, {"isbns":[{"raw":u"9788373087019",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '837308701X',
                                                                                                    'isbn13': '9788373087019',
                                                                                                    'core': '837308701'}]}

        yield self._test_validate_helper_eq, "ISBNs", {"isbns":u"978\u201183-7308-701-9"}, {"isbns":[{    "raw":"9788373087019",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '837308701X',
                                                                                                    'isbn13': '9788373087019',
                                                                                                    'core': '837308701'}]}


        yield self._test_validate_helper_eq, "ISBNs", {"isbns":u"978\u201183\u20127308\u2015701\u20159"}, {"isbns":[{    "raw":"9788373087019",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '837308701X',
                                                                                                    'isbn13': '9788373087019',
                                                                                                    'core': '837308701'}]}


        yield self._test_validate_helper_eq, "ISBNs", {"isbns":u"978\u201583\u20137308\u2011701\u20129"}, {"isbns":[{    "raw":"9788373087019",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '837308701X',
                                                                                                    'isbn13': '9788373087019',
                                                                                                    'core': '837308701'}]}

        yield self._test_validate_helper_info, "ISBNs", {"isbns":u"978\u201083\u20107308\u2010701\u20109"}
        yield self._test_validate_helper_info, "ISBNs", {"isbns":u"978\u201183-7308-701-9"}
        yield self._test_validate_helper_info, "ISBNs", {"isbns":u"978\u201183\u20127308\u2015701\u20159"}
        yield self._test_validate_helper_info, "ISBNs", {"isbns":u"978\u201583\u20137308\u2011701\u20129"}

        yield self._test_validate_helper_not_eq, "ISBNs", {"isbns":"9788373087019"}, {"isbns":[{    "raw":"9788373087019",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '',
                                                                                                    'isbn13': '9788373087019',
                                                                                                    'core': '837308701'}]}

        #Tests whether raw value is not write as core value
        yield self._test_validate_helper_not_eq, "ISBNs", {"isbns":"978-83-7308-701-9"}, {"isbns":[{"raw":"9788373087019",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '837308701X',
                                                                                                    'isbn13': '9788373087019',
                                                                                                    'core': '978-83-7308-701-9'}]}
        #Tests whether checksum digit is not write as 10
        yield self._test_validate_helper_not_eq, "ISBNs", {"isbns":"9788373087019"}, {"isbns":[{    "raw":"9788373087019",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '83730870110',
                                                                                                    'isbn13': '9788373087019',
                                                                                                    'core': '837308701'}]}

        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"0137-7566"}, {"isbns":[{'raw': '01377566', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"01377566"}, {"isbns":[{'raw': '01377566', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"0"}, {"isbns":[{'raw': '0', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"1"}, {"isbns":[{'raw': '1', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"12345"}, {"isbns":[{'raw': '12345', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"123456789"}, {"isbns":[{'raw': '123456789', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"123456789"}, {"isbns":[{'raw': '123456789', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"1234567890"}, {"isbns":[{'raw': '1234567890', 'valid': False, 'core': '123456789'}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"12345678901"}, {"isbns":[{'raw': '12345678901', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"1234"}, {"isbns":[{'raw': '1234', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"978-83-61445-20-5"}, {"isbns":[{'raw': '9788361445205', 'valid': False, 'core': '836144520'}]}

        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"ISBN978-83-936379-9-7"}, {"isbns":[{"raw":"9788393637997",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '8393637996',
                                                                                                    'isbn13': '9788393637997',
                                                                                                    'core': '839363799'}]}

        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"978-83-933966-0-4"}, {"isbns":[{'raw': '9788393396604', 'valid': False, 'core': '839339660'}]}

    def test_validate_authors(self):
        yield self._test_validate_helper_eq, "Authors", {}, {}
        yield self._test_validate_helper_eq, "Authors", {"authors":""}, {"persons":[{"authors":[]}]}
        yield self._test_validate_helper_eq, "Authors", {"authors":""}, {"persons":[{"authors":[]}]}
        yield self._test_validate_helper_eq, "Translators", {"translators":""}, {"persons":[{"translators":[]}]}
        yield self._test_validate_helper_eq, "Redactors", {"redactors":""}, {"persons":[{"redactors":[]}]}
        yield self._test_validate_helper_eq, "Lectors", {"lectors":""}, {"persons":[{"lectors":[]}]}

        yield self._test_validate_helper_raises, "Persons", {}, "asfasfas"
        yield self._test_validate_helper_raises, "Persons", {}, "author"
        yield self._test_validate_helper_raises, "Persons", {}, "translator"
        yield self._test_validate_helper_raises, "Persons", {}, "redactor"
        yield self._test_validate_helper_raises, "Persons", {}, "lector"


        yield self._test_validate_helper_eq, "Authors", {"authors":u"Mariola Jąder"}, {"persons":[{"authors":[{'name':u'Mariola Jąder', 'firstName': 'Mariola', 'middleName': u'', 'lastName': u'Jąder'}]}]}
        yield self._test_validate_helper_eq, "Authors", {"authors":u"Mariola  Jąder"}, {"persons":[{"authors":[{'name':u'Mariola Jąder', 'firstName': 'Mariola', 'middleName': u'', 'lastName': u'Jąder'}]}]}
        yield self._test_validate_helper_eq, "Authors", {"authors":u"Mariola Jąder"}, {"persons":[{"authors":[{'name':u'Mariola Jąder', 'firstName': 'Mariola', 'middleName': '', 'lastName': u'Jąder'}]}]}

        yield self._test_validate_helper_eq, "Authors", {"authors":u"Małgorzata Żmudzka-Kosała"}, {"persons":[{"authors":[{'name':u'Małgorzata Żmudzka-Kosała', 'firstName': u'Małgorzata', 'middleName': u'', 'lastName': u'Żmudzka-Kosała'}]}]}
        yield self._test_validate_helper_not_eq, "Authors", {"authors":u"Małgorzata Żmudzka-Kosała"}, {"persons":[{"authors":[{'name':u'Małgorzata Żmudzka-Kosała', 'firstName': 'Małgorzata', 'middleName': u'', 'lastName': u'Żmudzka-Kosała'}]}]}
        yield self._test_validate_helper_eq, "Authors", {"authors":u"Małgorzata Żmudzka - Kosała"}, {"persons":[{"authors":[{'name':u'Małgorzata Żmudzka-Kosała', 'firstName': u'Małgorzata', 'middleName': u'', 'lastName': u'Żmudzka-Kosała'}]}]}
        yield self._test_validate_helper_not_eq, "Authors", {"authors":u"Małgorzata Żmudzka - Kosała"}, {"persons":[{"authors":[{'name':u'Małgorzata Żmudzka - Kosała', 'firstName': 'Małgorzata', 'middleName': u'', 'lastName': u'Żmudzka - Kosała'}]}]}
        yield self._test_validate_helper_not_eq, "Authors", {"authors":u"Małgorzata Żmudzka - Kosała"}, {"persons":[{"authors":[{'name':u'Małgorzata Żmudzka - Kosała', 'firstName': 'Małgorzata', 'middleName': u'', 'lastName': u'Żmudzka-Kosała'}]}]}
        yield self._test_validate_helper_not_eq, "Authors", {"authors":u"Małgorzata Żmudzka - Kosała"}, {"persons":[{"authors":[{'name':u'Małgorzata Żmudzka - Kosała'}]}]}

        #yield self._test_validate_helper_not_eq, "Authors", {"authors":u"Red. Katarzyna Cymbalista-Hajib"}, {"authors":[{'middleName': u'Katarzyna', 'lastName': u'Cymbalista-Hajib', 'name': u'Red. Katarzyna Cymbalista-Hajib', 'firstName': u'Red.'}]}

        yield self._test_validate_helper_eq, "Authors", {"authors":u"J.Kobuszewski"}, {"persons":[{"authors":[{'name':u'J. Kobuszewski', 'firstName': 'J.', 'middleName': u'', 'lastName': u'Kobuszewski'}]}]}
        yield self._test_validate_helper_eq, "Authors", {"authors":u"S.J.Watson"}, {"persons":[{"authors":[{'name':u'S. J. Watson', 'firstName': 'S.', 'middleName': 'J.', 'lastName': u'Watson'}]}]}
        yield self._test_validate_helper_eq, "Authors", {"authors":u"George R.R.  Martin"}, {"persons":[{"authors":[{'middleName': u'', 'lastName': u'', 'name': u'George R. R. Martin', 'firstName': u''}]}]}

        yield self._test_validate_helper_eq, "Authors", {"authors":u"PIOTR CHOLEWIŃSKI"}, {"persons":[{"authors":[{'lastName': u'Cholewiński', 'name': u'PIOTR CHOLEWIŃSKI', 'middleName': u'', 'firstName': u'Piotr'}]}]}
        yield self._test_validate_helper_eq, "Authors", {"authors":u"H.Łabonarska"}, {"persons":[{"authors":[{'lastName': u'Łabonarska', 'name': u'H. Łabonarska', 'middleName': u'', 'firstName': u'H.'}]}]}
        yield self._test_validate_helper_eq, "Authors", {"authors":u"Wojciech Piotr  Kwiatek"}, {"persons":[{"authors":[{'lastName': 'Kwiatek', 'name': u'Wojciech Piotr Kwiatek', 'firstName': 'Wojciech', 'middleName': 'Piotr' }]}]}
        #yield self._test_validate_helper_eq, "Authors", {"authors":u"INFOA International s.r.o."}, {"authors":[{'name':u'INFOA International s.r.o.'}]}

        #ks. dr Krzysztof Marcyński SAC
        #redakcja Pons i Lektorklett
        #Edgar Allan  Poe
        #Beata i Bogdan Oczkowscy
        #E L  James
        #George R.R.  Martin
        #Roxanne  St. Claire
        #John Ronald R. Tolkien
        #Jakub i Wilhelm Grimm
        #Wilhelm i Jakub Grimm
        #Św. Jan od Krzyża

        yield self._test_validate_helper_eq, "Authors", {"authors":u"Tomasz Martyniuk;Barbara Dudek;Monika Wąs"}, {"persons":[{"authors":[
                                                                                                                              {'lastName': u'Martyniuk',
                                                                                                                               'name': u'Tomasz Martyniuk',
                                                                                                                               'middleName': u'',
                                                                                                                               'firstName': u'Tomasz'},

                                                                                                                              {'lastName': u'Dudek',
                                                                                                                               'name': u'Barbara Dudek',
                                                                                                                               'middleName': u'',
                                                                                                                               'firstName': u'Barbara'},

                                                                                                                              {'lastName': u'W\u0105s',
                                                                                                                               'name': u'Monika W\u0105s',
                                                                                                                               'middleName': u'',
                                                                                                                               'firstName': u'Monika'}
                                                                                                                              ]
                                                                                                                   }]}
