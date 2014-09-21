# -*- coding: utf-8 -*-
from decimal import Decimal
from django.test import TestCase
from django.utils.unittest.case import skip
from spistresci.model_controler import add_MiniBook
from spistresci.models import (
    Bookstore,
    BookstoreCommandStatus,
    BookFormat,
    BookFormatType,
    CommandStatus,
    MiniAuthor,
    MiniBook,
)


class TestAddBook(TestCase):

    # def test_basic_add_book(self):
    #
    #     bookstore, created = Bookstore.objects.get_or_create(**{'name':'TestowySklep', 'url': 'http://testowysklep.pl/'})
    #
    #     b1 = {
    #         'category': 'E-booki/Mlodziezowe',
    #         'publisher': 'Wydawnictwo e-bookowo',
    #         'description': {'description': 'testowy opis'},
    #         'title': 'Opowiesci o Malej Czarownicy Ismie',
    #         'url': u'http://ebooki.allegro.pl/ebook,b201.html',
    #         'b64_url': 'aHR0cDovL2Vib29raS5hbGxlZ3JvLnBsL2Vib29rLGIyMDEuaHRtbA==',
    #         'price': u'1520',
    #         'formats': [{'name': 'epub'}, {'name': 'mobi'}],
    #         'cover': u'http://ebooki.allegro.pl/imageshandler/201/miniature/',
    #         'authors': [{'middle_name': '', 'last_name': 'Ciepko', 'name': 'Aneta Ciepko', 'first_name': 'Aneta'}],
    #         #'book_type': None,
    #         'pp_url': u'http://www.a4b-tracking.com/pl/stat-click-text-link/56/120/aHR0cDovL2Vib29raS5hbGxlZ3JvLnBsL2Vib29rLGIyMDEuaHRtbA==',
    #         'isbns': [{'raw': u'9788362184409', 'valid': False, 'isbn10': u'8362184406', 'isbn13': u'9788362184409', 'core': u'836218440'}],
    #         'date': u'2012',
    #         'price_normal': u'-1',
    #         'external_id': u'219',
    #         'availability': u'1'
    #     }
    #
    #     add_MiniBook(bookstore, b1)
    #
    #     self.assertEqual(1 + 1, 2)

    def setUp(self):
        cmd_status = CommandStatus()
        cmd_status.save()

        self.test_bookstore_1 = Bookstore.objects.create(
            name='TestowySklep',
            url='http://testowysklep.pl/',
        )
        test_bookstore_1_cmd_status = BookstoreCommandStatus(
            cmd_status=cmd_status,
            bookstore=self.test_bookstore_1,
            type=BookstoreCommandStatus.TYPE_PARSE,
        )
        test_bookstore_1_cmd_status.save()

        self.test_bookstore_2 = Bookstore.objects.create(
            name='TestowySklep2',
            url='http://testowysklep2.pl/',
        )
        test_bookstore_2_cmd_status = BookstoreCommandStatus(
            cmd_status=cmd_status,
            bookstore=self.test_bookstore_2,
            type=BookstoreCommandStatus.TYPE_PARSE,
        )
        test_bookstore_2_cmd_status.save()


    def test_add_empty_book_to_empty_db(self):
        """
        test_add_empty_book_to_empty_db
        external_id=pods['external_id'] should fail (KeyError: 'external_id')
        """

        book = {}

        with self.assertRaises(KeyError):
            add_MiniBook(self.test_bookstore_1, book)

    def test_add_book_without_bookstore(self):
        """
        test_add_book_without_bookstore
        Cannot assign None: "MiniBook.bookstore" does not allow null values.
        """

        book = {
            'external_id': 1,
        }

        with self.assertRaises(ValueError):
            add_MiniBook(None, book)

    @skip("Don't want to test")
    def test_add_book_with_only_external_id_to_empty_db(self):
        """
        test_add_book_to_empty_db
        """

        book = {
            'external_id': 1,
        }

        book_1 = add_MiniBook(self.test_bookstore_1, book)
        self.assertEquals(book_1.external_id, 1)

        columns = MiniBook._meta.get_all_field_names()

        columns_without_defaults = [
            'id',
            'external_id',
            'bookstore',
            'created',
            'modified',
        ]

        pods_defaults = {
            'title': '',
            'cover': '',
            'price': Decimal('0.00'),
            'price_normal': Decimal('0.00'),
            'url': '',
            'pp_url': '',
            'extra': {},
        }

        columns = [
            col
            for col in columns
            if col not in columns_without_defaults
        ]

        for column in columns:
            field_tuple = MiniBook._meta.get_field_by_name(column)

            field = field_tuple[0]
            m2m = field_tuple[3]

            if field.rel:
                if m2m:
                    self.assertEquals(
                        list(getattr(book_1, column).all()),
                        [],
                        "%s != []" % column,
                    )
                else:
                    self.assertEquals(
                        getattr(book_1, column),
                        None,
                        "%s != None" % column,
                    )
            else:
                self.assertEquals(
                    getattr(book_1, column) == pods_defaults[column],
                    True,
                    "%s != %s" % (column, str(pods_defaults[column])),
                )

    def test_two_books_from_diff_bookstores_with_this_same_external_id(self):

        book = {
            'external_id': 3,
        }
        self.assertEquals(MiniBook.objects.count(), 0)

        book_1 = add_MiniBook(self.test_bookstore_1, book)
        book_2 = add_MiniBook(self.test_bookstore_2, book)

        self.assertNotEqual(book_1, book_2)
        self.assertEquals(MiniBook.objects.count(), 2)

    def test_two_books_from_one_bookstore_with_this_same_external_id(self):

        book = {
            'external_id': 4,
        }
        self.assertEquals(MiniBook.objects.count(), 0)

        book_1 = add_MiniBook(self.test_bookstore_1, book)
        book_2 = add_MiniBook(self.test_bookstore_1, book)

        self.assertEqual(book_1, book_2)
        self.assertEquals(MiniBook.objects.count(), 1)

    def test_update_of_title(self):

        book = {
            'external_id': 5,
            'title': 'old title'
        }
        self.assertEquals(MiniBook.objects.count(), 0)

        book_1 = add_MiniBook(self.test_bookstore_1, book)
        self.assertEqual(book_1.title, 'old title')

        book['title'] = 'new title'
        book_2 = add_MiniBook(self.test_bookstore_1, book)
        self.assertEquals(MiniBook.objects.count(), 1)

        self.assertEqual(book_1, book_2)
        self.assertEqual(book_2.title, 'new title')


    def test_update_of_external_id(self):

        book = {
            'external_id': 6,
            'title': 'old title'
        }
        self.assertEquals(MiniBook.objects.count(), 0)

        book_1 = add_MiniBook(self.test_bookstore_1, book)
        self.assertEqual(book_1.external_id, 6)

        book['external_id'] = 7

        book_2 = add_MiniBook(self.test_bookstore_1, book)
        self.assertNotEqual(book_1, book_2)

        self.assertEqual(book_1.external_id, 6)
        self.assertEqual(book_2.external_id, 7)

        self.assertEquals(MiniBook.objects.count(), 2)

    def test_add_book_with_empty_list_of_formats(self):

        book_dict_1 = {
            'external_id': u'17',
        }

        book_1 = add_MiniBook(self.test_bookstore_1, book_dict_1)
        self.assertEquals(book_1.formats.count(), 0)

        book_dict_1['formats'] = []
        book_1 = add_MiniBook(self.test_bookstore_1, book_dict_1)
        self.assertEquals(book_1.formats.count(), 0)

    def test_update_of_new_format(self):

        book_format_name = 'testf'

        with self.assertRaises(BookFormat.DoesNotExist):
            BookFormat.objects.get(name=book_format_name)

        number_of_formats = BookFormat.objects.count()

        ebook = BookFormatType.objects.get(name='ebook')

        book_dict_1 = {
            'external_id': u'16',
            'formats': [
                {
                    'name': book_format_name,
                    'type': ebook
                },
            ],
        }

        book_1 = add_MiniBook(self.test_bookstore_1, book_dict_1)
        self.assertEquals(book_1.formats.count(), 1)
        self.assertEquals(BookFormat.objects.count(), number_of_formats + 1)

    def test_update_of_existing_format(self):

        book_format_name = 'mobi'
        BookFormat.objects.get(name=book_format_name)
        number_of_formats = BookFormat.objects.count()
        ebook = BookFormatType.objects.get(name='ebook')

        book_dict_1 = {
            'external_id': u'16',
            'formats': [
                {
                    'name': book_format_name,
                    'type': ebook
                },
            ],
        }

        book_1 = add_MiniBook(self.test_bookstore_1, book_dict_1)
        self.assertEquals(book_1.formats.count(), 1)
        self.assertEquals(BookFormat.objects.count(), number_of_formats)

    def test_two_new_formats_instead_one_old_format(self):

        ebook = BookFormatType.objects.get(name='ebook')

        book_dict_1 = {
            'external_id': u'16',
            'formats': [{'name': 'epub', 'type': ebook}],
        }

        book_1 = add_MiniBook(self.test_bookstore_1, book_dict_1)
        self.assertEquals(book_1.formats.count(), 1)

        book_dict_1['formats'] = [
            {'name': 'mobi', 'type': ebook},
            {'name': 'pdf', 'type': ebook}
        ]
        book_1 = add_MiniBook(self.test_bookstore_1, book_dict_1)
        self.assertEquals(book_1.formats.count(), 2)

    def test_add_author(self):

        book = {
            'external_id': 1,
            'authors': [{
                'middle_name': '',
                'last_name': 'Ciepko',
                'name': 'Aneta Ciepko',
                'first_name': 'Aneta',
            }],
        }

        self.assertEquals(MiniAuthor.objects.count(), 0)
        book_1 = add_MiniBook(self.test_bookstore_1, book)
        self.assertEquals(MiniAuthor.objects.count(), 1)

        author = book_1.authors.all()[0]

        self.assertEquals(author.middle_name, '')
        self.assertEquals(author.last_name, 'Ciepko')
        self.assertEquals(author.name, 'Aneta Ciepko')
        self.assertEquals(author.first_name, 'Aneta')

    def test_modify_author(self):

        author_dict = {
            'middle_name': '',
            'last_name': 'Ciepko',
            'name': 'Aneta Ciepko',
            'first_name': 'Aneta',
        }

        book = {
            'external_id': 1,
            'authors': [author_dict],
        }

        self.assertEquals(MiniAuthor.objects.count(), 0)
        book_1 = add_MiniBook(self.test_bookstore_1, book)
        self.assertEquals(book_1.authors.count(), 1)
        self.assertEquals(MiniAuthor.objects.count(), 1)

        author1 = book_1.authors.all()[0]
        self.assertEquals(author1.last_name, 'Ciepko')

        author_dict['last_name'] = 'Smith'
        book_2 = add_MiniBook(self.test_bookstore_1, book)
        self.assertEquals(book_2.authors.count(), 1)
        self.assertEquals(MiniAuthor.objects.count(), 2)

        author2 = book_1.authors.all()[0]
        self.assertNotEqual(author1, author2)

        self.assertEquals(author2.last_name, 'Smith')
