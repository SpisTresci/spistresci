# -*- coding: utf-8 -*-
from django.test import TestCase

from os.path import abspath, dirname, join

from spistresci.connectors.specific.Publio import Publio
from spistresci.models import (
    BookstoreCommandStatus,
    CommandStatus,
    MiniBook,
)


class TestConnectorParse(TestCase):

    def setUp(self):
        self.connector = Publio()

        cmd_status = CommandStatus()
        cmd_status.save()

        bookstore_cmd_status = BookstoreCommandStatus(
            cmd_status=cmd_status,
            bookstore=self.connector.bookstore,
            type=BookstoreCommandStatus.TYPE_PARSE,
        )

        self.connector.bookstore_cmd_status = bookstore_cmd_status

        bookstore_cmd_status.save()

        fetched_file = join(
            dirname(abspath(__file__)),
            'xmls',
            '%s.xml' % self.connector.name.lower(),
        )

        self.connector.fetched_files = [fetched_file]
        self.connector.areDataDifferentThanPrevious = lambda: True
        self.connector.parse()

    def test_publio_parse(self):
        publio_mini_count = MiniBook.objects.filter(
            bookstore=self.connector.bookstore
        ).count()
        self.assertEquals(publio_mini_count, 5)
