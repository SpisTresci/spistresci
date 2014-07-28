from django.core import management
from django.test import TestCase


class DeleteOrphanRecordsManagementCommandTest(TestCase):

    def setUp(self):
        pass

    def test_call_command(self):
        management.call_command('deleteorphanrecords')
