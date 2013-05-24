import nose
from nose.tools import *
from utils import NoseUtils
from utils import DataValidator, DataValidatorError

class MockErratumLogger():
    warned = False
    def warning(self, str):
        self.warned = True

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

    def test_validate_format(self):
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
