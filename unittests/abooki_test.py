from connectors.specific import Abooki
from nose.tools import *
from unittests.data_validator import MockErratumLogger


class MockAbooki(Abooki):
    def __init__(self):
        self.logger = None
        self.backup_dir = None
        self.unpack_dir = None
        self.supported_formats = ['cd','mp3', 'dvd']
        self.accepted_suffix_patterns = ' *,-'
        self.erratum_logger = MockErratumLogger()
        self._name = 'MockAbooki'


class TestAbookiConnector(object):
    def setUp(self):
        self.ma = MockAbooki()
        pass

    def tearDown(self):
        pass

    @nottest
    def _test_adjust_parse(self, dic, expected):
        self.ma.adjust_parse(dic)
        eq_(dic, expected)

    def test_adjust_parse(self):
       titles = [{'title':'dummy1'},
       {'title':'dummy,123cd'},
       {'title':'dummy,123,456dvd-cd'},
       {'title':'dummy    ,    11    mp3'},
       {'title':'cd'},
       {'title':'cd,cd,11'},
       {'title':'cd,cd,11mp3'},
       ]
       expected = [{'title': 'dummy1', 'formats': ''},
       {'title':'dummy', 'formats':'123cd'},
       {'title':'dummy,123', 'formats':'456dvd-cd'},
       {'title':'dummy','formats':'11    mp3'},
       {'title':'cd', 'formats':''},
       {'title':'cd,cd,11', 'formats':''},
       {'title':'cd,cd', 'formats':'11mp3'},
       ]
       for (dic, exp) in zip(titles, expected):
           yield self._test_adjust_parse, dic, exp

    @nottest
    def _test_validate_formats(self, dic, expected_formats, check_erratum = False):
       self.ma.validateFormats(dic, 'dummy', 'dummy')
       eq_(dic['formats'], expected_formats)
       if check_erratum:
           assert(self.ma.erratum_logger.warned)
       else:
           eq_(self.ma.erratum_logger.warned, False)

    def test_validate_formats(self):
        dicts = [{'formats':'cd dvd mp3'},
        {'formats': 'cd   dvd    -----'},
        {'formats':'    '},
        ]

        expected_formats = [['cd', 'mp3', 'dvd'],
        ['cd', 'dvd'],
        [],
        ]
        for (dic, exp) in zip(dicts, expected_formats):
            yield self._test_validate_formats, dic, exp

    def test_validate_wrong_formats(self):
        dicts = [{'formats':'cd dvd mp3aaa'},
        {'formats': 'cd dvd dummy_bad_format     '},
        {'formats':'dummy_bad_format'},
        ]

        expected_formats = [['cd', 'mp3', 'dvd'],
        ['cd', 'dvd'],
        [],
        ]
        for (dic, exp) in zip(dicts, expected_formats):
            yield self._test_validate_formats, dic, exp, True
