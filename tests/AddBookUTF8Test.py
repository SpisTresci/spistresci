# -*- coding: utf-8 -*-
from django.test import TestCase
from spistresci.model_controler import add_MiniBook
from spistresci.models import (
    Bookstore,
    MiniAuthor,
    MiniBook,
)


class AddBookUTF8Test(TestCase):
    """
    Test for checking utf8 capability,
    In case of any failures, please see:
    http://stackoverflow.com/a/10866836/338581
    """

    def setUp(self):

        self.test_bookstore_utf8_1 = Bookstore.objects.create(
            name=u'Żółty żółw',
            url=u'http://żółty-żółw.pl/',
        )

    def test_title_in_utf8(self):

        book = {
            'external_id': 1,
            'title': u'Powieść kończąca się kropką'
        }
        self.assertEquals(MiniBook.objects.count(), 0)

        book_1 = add_MiniBook(self.test_bookstore_utf8_1, book)
        self.assertEquals(MiniBook.objects.count(), 1)
        self.assertEquals(book_1.title, book['title'])

    def test_add_author_in_utf8(self):

        book = {
            'external_id': 1,
            'authors': [{
                'name': u'Małgorzata Elżbieta Kalicińska',
                'first_name': u'Małgorzata',
                'middle_name': u'Elżbieta',
                'last_name': u'Kalicińska',
            }],
        }

        self.assertEquals(MiniAuthor.objects.count(), 0)
        book_1 = add_MiniBook(self.test_bookstore_utf8_1, book)
        self.assertEquals(MiniAuthor.objects.count(), 1)

        author = MiniAuthor.objects.all()[0]

        self.assertEquals(author.name, u'Małgorzata Elżbieta Kalicińska')
        self.assertEquals(author.first_name, u'Małgorzata')
        self.assertEquals(author.middle_name, u'Elżbieta')
        self.assertEquals(author.last_name, u'Kalicińska')
