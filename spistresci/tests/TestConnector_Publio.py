# -*- coding: utf-8 -*-
from django.test import TestCase

from spistresci.connectors.specific.Publio import Publio


class TestConnector_Publio(TestCase):

    def setUp(self):
        self.connector = Publio()

    def test_publio_validateISBNs__one_isbn(self):

        dic = {
            'isbns': '978-837-961-694-7'
        }

        self.connector.validateISBNs(dic, 42, 'example title')

        expected_dict = {
            'isbns': [
                {
                    'raw': '9788379616947',
                    'valid': True,
                    'isbn10': '8379616944',
                    'isbn13': '9788379616947',
                    'core': '837961694'
                }
            ]
        }

        self.assertEquals(dic, expected_dict)

    def test_publio_validateISBNs__multiple_isbns(self):

        dic = {
            'isbns': '978-832-681-346-7, 978-832-681-671-0, 978-832-681-672-7'
        }

        self.connector.validateISBNs(dic, 42, 'example title')

        expected_dict = {
            'isbns': [
                {
                    'raw': '9788326813467',
                    'valid': True,
                    'isbn10': '832681346X',
                    'isbn13': '9788326813467',
                    'core': '832681346'
                },
                {
                    'raw': '9788326816710',
                    'valid': True,
                    'isbn10': '832681671X',
                    'isbn13': '9788326816710',
                    'core': '832681671'
                },
                {
                    'raw': '9788326816727',
                    'valid': True,
                    'isbn10': '8326816728',
                    'isbn13': '9788326816727',
                    'core': '832681672'
                }
            ]
        }

        self.assertEquals(dic, expected_dict)

    def test_publio_adjust_parse__one_category(self):

        dic = {'category': u'Powieść, opowiadanie'}
        expected_dict = {'category': u'Powieść, opowiadanie'}

        self.connector.adjust_parse(dic)

        self.assertEquals(dic, expected_dict)

    def test_publio_adjust_parse__multiple_category(self):

        dic = {
            'category': [
                u'Powie\u015b\u0107, opowiadanie',
                u'Krymina\u0142, thriller',
                u'Thriller',
                u'Thriller religijny',
                u'Thriller spiskowy'
            ]
        }

        expected_dict = {
            'category': u'Powieść, opowiadanie, Kryminał, thriller, Thriller, Thriller religijny, Thriller spiskowy'  # nopep8
        }

        self.connector.adjust_parse(dic)

        self.assertEquals(dic, expected_dict)
