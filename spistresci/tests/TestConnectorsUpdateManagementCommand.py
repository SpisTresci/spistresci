from django.core import management
from django.test import TestCase
from unittest.case import skip


class ConnectorsUpdateManagementCommandTest(TestCase):

    def setUp(self):
        pass

    @skip("do not test this yet")
    def test_call_command(self):
        management.call_command('connectorsupdate', mode='test')

    @skip("do not test this yet")
    def test_missing_settings_in_ini_file(self):
        raise NotImplementedError()

    @skip("do not test this yet")
    def test_connectors_read_from_ini_file(self):
        raise NotImplementedError()

    @skip("do not test this yet")
    def test_command_status_and_error_during_fetch(self):
        raise NotImplementedError()

    @skip("do not test this yet")
    def test_command_status_and_error_during_parse(self):
        raise NotImplementedError()
