from connectors.specific import Abooki
from nose.tools import *
from unittests.data_validator import MockErratumLogger
from format_in_title_connectors_base import FormatInTitleTestFixture 

class MockAbooki(Abooki):
    def __init__(self):
        self.logger = None
        self.backup_dir = None
        self.unpack_dir = None
        self.supported_formats = ['cd','mp3', 'dvd']
        self.accepted_suffix_patterns = ' *,-'
        self.erratum_logger = MockErratumLogger()
        self._name = 'MockAbooki'


class TestAbookiConnector(FormatInTitleTestFixture):
    def setUp(self):
        self.connector= MockAbooki()
