from connectors.specific import Audiobook
from nose.tools import *
from unittests.data_validator import MockErratumLogger
from format_in_title_connectors_base import FormatInTitleTestFixture 

class MockAudiobook(Audiobook):
    def __init__(self):
        self.logger = None
        self.backup_dir = None
        self.unpack_dir = None
        self.supported_formats = ['cd','mp3', 'dvd']
        self.accepted_suffix_patterns = ' *,-'
        self.erratum_logger = MockErratumLogger()
        self._name = 'MockAudiobook'
        self.format_in_title_split_regex = ',|\+'


class TestAudiobookConnector(FormatInTitleTestFixture):
    def setUp(self):
        self.connector= MockAudiobook()

    def test_adjust_parse(self):
       titles = [{'title':'dummy1'},
       {'title':'dummy,123cd'},
       {'title':'dummy,123,456dvd-cd'},
       {'title':'dummy    ,    11    mp3'},
       {'title':'cd'},
       {'title':'cd,cd,11'},
       {'title':'cd,cd,11mp3'},
       {'title':'cd+cd+11mp3-  '},
       {'title':'cd+cd+11mp3-  '},
       {'title':'cd-cd+11mp3-  '},
       ]
       expected = [{'title': 'dummy1', 'formats': '', 'cover': ''},
       {'title':'dummy', 'formats':'123cd', 'cover': ''},
       {'title':'dummy,123', 'formats':'456dvd-cd', 'cover': ''},
       {'title':'dummy','formats':'11    mp3', 'cover': ''},
       {'title':'cd', 'formats':'', 'cover': ''},
       {'title':'cd,cd,11', 'formats':'', 'cover': ''},
       {'title':'cd,cd', 'formats':'11mp3', 'cover': ''},
       {'title':'cd+cd', 'formats':'11mp3-', 'cover': ''},
       {'title':'cd+cd', 'formats':'11mp3-', 'cover': ''},
       {'title':'cd-cd', 'formats':'11mp3-', 'cover': ''},

       ]
       for (dic, exp) in zip(titles, expected):
           yield self._test_adjust_parse, dic, exp
