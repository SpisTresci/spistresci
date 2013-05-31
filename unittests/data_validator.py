import nose
from nose.tools import *
from utils import NoseUtils
from utils import DataValidator, DataValidatorError

class MockErratumLogger():
    warned = False
    informed = False
    def warning(self, str):
        self.warned = True

    def info(self, str):
        self.informed = True

class TestDataValidator():

    def setUp(self):
        self.dv = DataValidator()
        self.dv.erratum_logger = MockErratumLogger()
        self.dv.name = "TestDataValidator"

    @nottest
    def _test_validate_helper_eq(self, functionName, input, expected):
        validateFun = getattr(self.dv, "validate" + functionName)
        validateFun(input, "id", "title")
        eq_(input, expected)

    @nottest
    def _test_validate_helper_not_eq(self, functionName, input, expected):
        validateFun = getattr(self.dv, "validate" + functionName)
        validateFun(input, "id", "title")
        assert input != expected

    @nottest
    def _test_validate_helper_warning(self, functionName, input):
        eq_(self.dv.erratum_logger.warned, False)
        validateFun = getattr(self.dv, "validate" + functionName)
        validateFun(input, "id", "title")
        eq_(self.dv.erratum_logger.warned, True)
        self.dv.erratum_logger.warned = False
        eq_(self.dv.erratum_logger.warned, False)

    @nottest
    def _test_validate_helper_info(self, functionName, input):
        eq_(self.dv.erratum_logger.informed, False)
        validateFun = getattr(self.dv, "validate" + functionName)
        validateFun(input, "id", "title")
        eq_(self.dv.erratum_logger.informed, True)
        self.dv.erratum_logger.informed = False
        eq_(self.dv.erratum_logger.informed, False)

    @nottest
    @raises(DataValidatorError)
    def _test_validate_helper_raises(self, functionName, input):
        validateFun = getattr(self.dv, "validate" + functionName)
        validateFun(input, "id", "title")

    def test_validate_price(self):
        yield self._test_validate_helper_eq, "Price", {}, {"price":"0"}
        yield self._test_validate_helper_eq, "Price", {"price":"1000"}, {"price":"1000"}
        yield self._test_validate_helper_eq, "Price", {"price":"000"}, {"price":"0"}
        yield self._test_validate_helper_eq, "Price", {"price":"0"}, {"price":"0"}

        yield self._test_validate_helper_eq, "Price", {"price":"9.99"}, {"price":"999"}
        yield self._test_validate_helper_eq, "Price", {"price":"734.00"}, {"price":"73400"}
        yield self._test_validate_helper_eq, "Price", {"price":"1.00"}, {"price":"100"}
        yield self._test_validate_helper_eq, "Price", {"price":"0,17"}, {"price":"17"}
        yield self._test_validate_helper_eq, "Price", {"price":"0,09"}, {"price":"9"}

        yield self._test_validate_helper_eq, "Price", {"price":"9,99"}, {"price":"999"}
        yield self._test_validate_helper_eq, "Price", {"price":"734,00"}, {"price":"73400"}
        yield self._test_validate_helper_eq, "Price", {"price":"1,23"}, {"price":"123"}
        yield self._test_validate_helper_eq, "Price", {"price":"0,42"}, {"price":"42"}
        yield self._test_validate_helper_eq, "Price", {"price":"0,01"}, {"price":"1"}
        yield self._test_validate_helper_eq, "Price", {"price":"0.00"}, {"price":"0"}

        yield self._test_validate_helper_not_eq, "Price", {"price":"0,01"}, {"price":"001"}

        yield self._test_validate_helper_warning, "Price", {"price":"-5"}
        yield self._test_validate_helper_warning, "Price", {"price":"-5.57"}
        yield self._test_validate_helper_warning, "Price", {"price":"4.999"}
        yield self._test_validate_helper_warning, "Price", {"price":"4.999"}
        yield self._test_validate_helper_warning, "Price", {"price":"0,,01"}
        yield self._test_validate_helper_warning, "Price", {"price":"5,574,547"}
        yield self._test_validate_helper_warning, "Price", {"price":"5.574.547"}
        yield self._test_validate_helper_warning, "Price", {"price":"9.123456"}
        yield self._test_validate_helper_warning, "Price", {"price":".00"}
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
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"978-83-7308-701-9"}, {"isbns":[{    "raw":"978-83-7308-701-9",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '837308701X',
                                                                                                    'isbn13': '9788373087019',
                                                                                                    'core': '837308701'}]}

        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"978-83-7308-701-9"}, {"isbns":[{    "raw":"978-83-7308-701-9",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '837308701X',
                                                                                                    'isbn13': '9788373087019',
                                                                                                    'core': '837308701'}]}

        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"9788373087019"}, {"isbns":[{        "raw":"9788373087019",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '837308701X',
                                                                                                    'isbn13': '9788373087019',
                                                                                                    'core': '837308701'}]}

        yield self._test_validate_helper_not_eq, "ISBNs", {"isbns":"978-83-7308-701-9"}, {"isbns":[{ "raw":"9788373087019",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '837308701X',
                                                                                                    'isbn13': '9788373087019',
                                                                                                    'core': '837308701'}]}

        yield self._test_validate_helper_not_eq, "ISBNs", {"isbns":"9788373087019"}, {"isbns":[{    "raw":"9788373087019",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '',
                                                                                                    'isbn13': '9788373087019',
                                                                                                    'core': '837308701'}]}

        #Tests whether raw value is not write as core value
        yield self._test_validate_helper_not_eq, "ISBNs", {"isbns":"978-83-7308-701-9"}, {"isbns":[{"raw":"978-83-7308-701-9",
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

        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"0137-7566"}, {"isbns":[{'raw': '0137-7566', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"01377566"}, {"isbns":[{'raw': '01377566', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"0"}, {"isbns":[{'raw': '0', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"1"}, {"isbns":[{'raw': '1', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"12345"}, {"isbns":[{'raw': '12345', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"123456789"}, {"isbns":[{'raw': '123456789', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"123456789"}, {"isbns":[{'raw': '123456789', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"1234567890"}, {"isbns":[{'raw': '1234567890', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"12345678901"}, {"isbns":[{'raw': '12345678901', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"1234"}, {"isbns":[{'raw': '1234', 'valid': False}]}
        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"978-83-61445-20-5"}, {"isbns":[{'raw': '978-83-61445-20-5', 'valid': False}]}

        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"ISBN978-83-936379-9-7"}, {"isbns":[{"raw":"978-83-936379-9-7",
                                                                                                    'valid': True,
                                                                                                    'isbn10': '8393637996',
                                                                                                    'isbn13': '9788393637997',
                                                                                                    'core': '839363799'}]}

        yield self._test_validate_helper_eq, "ISBNs", {"isbns":"978-83-933966-0-4"}, {"isbns":[{'raw': '978-83-933966-0-4', 'valid': False}]}
