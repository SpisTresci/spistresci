# -*- coding: utf-8 -*-
from django.test import TestCase

from os.path import abspath, dirname, join
from spistresci.connectors.specific import (
    Allegro,
    Gandalf,
    Publio,
    Woblink,
)

from spistresci.models import (
    Bookstore,
    BookstoreCommandStatus,
    CommandStatus,
    MiniBook,
)


class TestConnectorAnalyze(TestCase):

    def setUp(self):

        connectors = [
            Allegro,
            Gandalf,
            Publio,
            Woblink,
        ]

        for __connector__ in connectors:

            connector = __connector__()

            cmd_status = CommandStatus()
            cmd_status.save()

            bookstore_cmd_status = BookstoreCommandStatus(
                cmd_status=cmd_status,
                bookstore=connector.bookstore,
                type=BookstoreCommandStatus.TYPE_PARSE,
            )

            connector.bookstore_cmd_status = bookstore_cmd_status

            bookstore_cmd_status.save()

            fetched_file = join(
                dirname(abspath(__file__)),
                'xmls',
                '%s.xml' % connector.name.lower(),
            )

            connector.fetched_files = [fetched_file]
            connector.areDataDifferentThanPrevious = lambda: True
            connector.parse()

    def test_allegro_parse(self):

        bookstore = Bookstore.objects.get(name='Allegro')

        allegro_mini_count = MiniBook.objects.filter(
            bookstore=bookstore
        ).count()
        self.assertEquals(allegro_mini_count, 2)

    def test_gandalf_parse(self):

        bookstore = Bookstore.objects.get(name='Gandalf')

        gandalf_mini_count = MiniBook.objects.filter(
            bookstore=bookstore
        ).count()
        self.assertEquals(gandalf_mini_count, 4)

    def test_publio_parse(self):

        bookstore = Bookstore.objects.get(name='Publio')

        publio_mini_count = MiniBook.objects.filter(
            bookstore=bookstore
        ).count()
        self.assertEquals(publio_mini_count, 5)

    def test_woblink_parse(self):

        bookstore = Bookstore.objects.get(name='Woblink')

        woblink_mini_count = MiniBook.objects.filter(
            bookstore=bookstore
        ).count()
        self.assertEquals(woblink_mini_count, 3)

    def test_getCandidatesByTitle__Allegro_Tlumaczka(self):

        mini_book = MiniBook.objects.get(
            bookstore=Bookstore.objects.get(name='Allegro'),
            external_id=19033
        )

        self.assertEquals(mini_book.title, u'Tłumaczka')

        candidates = mini_book.getCandidatesByTitle()

        self.assertEquals(candidates.count(), 1)

        expected_bookstores = ['Gandalf']

        for candidate in candidates:
            self.assertIn(candidate.bookstore.name, expected_bookstores)

    def test_getCandidatesByTitle__Publio_Anioly_i_Demony(self):

        mini_book = MiniBook.objects.get(
            bookstore=Bookstore.objects.get(name='Publio'),
            external_id=87901
        )

        self.assertEquals(mini_book.title, u'Anioły i demony')

        candidates = mini_book.getCandidatesByTitle()

        self.assertEquals(candidates.count(), 2)

        expected_bookstores = ['Gandalf', 'Woblink']

        for candidate in candidates:
            self.assertIn(candidate.bookstore.name, expected_bookstores)

    def test_getCandidatesByTitle__Woblink_Inferno(self):

        mini_book = MiniBook.objects.get(
            bookstore=Bookstore.objects.get(name='Woblink'),
            external_id=10322
        )

        self.assertEquals(mini_book.title, u'Inferno')

        candidates = mini_book.getCandidatesByTitle()

        self.assertEquals(candidates.count(), 3)

        expected_bookstores = ['Allegro', 'Gandalf', 'Publio']

        for candidate in candidates:
            self.assertIn(candidate.bookstore.name, expected_bookstores)
