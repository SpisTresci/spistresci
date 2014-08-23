# -*- coding: utf-8 -*-
from decimal import Decimal

from django.test import TestCase

from ddt import ddt, data
from nose.tools import (
    eq_,
    nottest,
    raises,
)

from spistresci.connectors.utils.DataValidator import DataValidator


class MockErratumLogger(object):

    def __init__(self):
        self.warned = False
        self.informed = False
        self.debug_informed = False
        self.warntext = ''
        self.infotext = ''
        self.debugtext = ''

    def warning(self, text):
        self.warned = True
        self.warntext = text

    def info(self, text):
        self.informed = True
        self.infotext = text

    def debug(self, text):
        self.debug_informed = True
        self.debugtext = text


@ddt
class TestDataValidator(TestCase):

    def setUp(self):
        self.dv = DataValidator()
        self.dv.erratum_logger = MockErratumLogger()
        self.dv.name = "TestDataValidator"

    @nottest
    def validate_eq(self, function_name, dic, expected, *args, **kwargs):
        validate_fun = getattr(self.dv, "validate" + function_name)
        validate_fun(dic, "id", "title", *args, **kwargs)
        self.assertEqual(dic, expected)

    @nottest
    def validate_not_eq(self, function_name, dic, expected, *args, **kwargs):
        validate_fun = getattr(self.dv, "validate" + function_name)
        validate_fun(dic, "id", "title", *args, **kwargs)
        self.assertNotEqual(dic, expected)

    @nottest
    def validate_warning(self, function_name, dic, *args, **kwargs):
        eq_(self.dv.erratum_logger.warned, False)
        validate_fun = getattr(self.dv, "validate" + function_name)
        validate_fun(dic, "id", "title", *args, **kwargs)
        self.assertEqual(self.dv.erratum_logger.warned, True)
        self.dv.erratum_logger.warned = False
        self.assertEqual(self.dv.erratum_logger.warned, False)

    @nottest
    def validate_info(self, function_name, dic, *args, **kwargs):
        eq_(self.dv.erratum_logger.informed, False)
        validate_fun = getattr(self.dv, "validate" + function_name)
        validate_fun(dic, "id", "title", *args, **kwargs)
        self.assertEqual(self.dv.erratum_logger.informed, True)
        self.dv.erratum_logger.informed = False
        self.assertEqual(self.dv.erratum_logger.informed, False)

    @nottest
    @raises(Exception)
    def validate_raises(self, function_name, dic,  *args, **kwargs):
        validate_fun = getattr(self.dv, "validate" + function_name)
        validate_fun(dic, "id", "title", *args, **kwargs)

    @data(
        # converted to 0.00
        (
            {},
            {'price': Decimal('0.0')}
        ),
        (
            {'price': ''},
            {'price': Decimal('0.0')}
        ),
        (
            {'price': '0'},
            {'price': Decimal('0.00')}
        ),
        (
            {'price': '00'},
            {'price': Decimal('0.00')}
        ),
        (
            {'price': '.00'},
            {'price': Decimal('0.00')}
        ),
        (
            {'price': '0.00'},
            {'price': Decimal('0.00')}
        ),

        # usual cases
        (
            {'price': '10'},
            {'price': Decimal('10.00')}
        ),
        (
            {'price': '124'},
            {'price': Decimal('124.00')}
        ),
        (
            {'price': '73.4'},
            {'price': Decimal('73.40')}
        ),
        (
            {'price': '9.99'},
            {'price': Decimal('9.99')}
        ),
        (
            {'price': '0.17'},
            {'price': Decimal('0.17')}
        ),
        (
            {'price': '0.09'},
            {'price': Decimal('0.09')}
        ),
        (
            {'price': '.99'},
            {'price': Decimal('0.99')}
        ),

        # , instead of .
        (
            {'price': '73,4'},
            {'price': Decimal('73.40')}
        ),
        (
            {'price': '9,99'},
            {'price': Decimal('9.99')}
        ),
        (
            {'price': '0,17'},
            {'price': Decimal('0.17')}
        ),
        (
            {'price': '0,09'},
            {'price': Decimal('0.09')}
        ),
        (
            {'price': ',99'},
            {'price': Decimal('0.99')}
        ),

        #zinamon prices fix - truncate prices to gr
        (
            {'price': '2.120001'},
            {'price': Decimal('2.12')}
        ),
        (
            {'price': '2.120099'},
            {'price': Decimal('2.12')}
        ),
        (
            {'price': '.1200'},
            {'price': Decimal('0.12')}
        ),
        (
            {'price': '01231321.1200'},
            {'price': Decimal('1231321.12')}
        ),

        # Default price
        # TODO: consider what should happen if id tag is empty,
        # currently it is replaced by defalt_price
        (
            {},
            {'price': Decimal('1.00')},
            'price',
            '1.00'
        ),
        (
            {'price': ''},
            {'price': Decimal('1.00')},
            'price',
            '1.00'
        ),
    )
    def test_validate_price_eq(self, args):
        self.validate_eq('Price', *args)

    @data(
        {'price': '-5'},
        {'price': '-5.57'},
        {'price': '0,,01'},
        {'price': '5.574.547'},
        {'price': '20 zl'},
    )
    def test_validate_price_warning(self, value1):
        self.validate_warning('Price', value1)

    @data(
        ({}, 'price', 'NOT_INT'),
    )
    def test_validate_price_raises(self, args):
        self.validate_raises('Price', *args)

    @data(
        (
            {},
            {}
        ),
        (
            {
                'authors': ''
            },
            {
                'authors': [],
            }
        ),
        (
            {
                'authors': u'George R.R.  Martin'
            },
            {
                'authors': [
                    {
                        'name': u'George R. R. Martin',
                        'first_name': u'',
                        'middle_name': u'',
                        'last_name': u'',
                    }
                ]
            }
        ),
        (
            {
                'authors': u'Mariola Jąder'
            },
            {
                'authors': [
                    {
                        'name': u'Mariola Jąder',
                        'first_name': 'Mariola',
                        'middle_name': u'',
                        'last_name': u'Jąder'
                    }
                ]
            }
        ),
        (
            {
                'authors': u'Mariola  Jąder'
            },
            {
                'authors': [
                    {
                        'name': u'Mariola Jąder',
                        'first_name': 'Mariola',
                        'middle_name': '',
                        'last_name': u'Jąder'
                    }
                ]
            }
        ),
        (
            {'authors': u'Mariola Jąder'},
            {
                'authors': [
                    {
                        'name': u'Mariola Jąder',
                        'first_name': u'Mariola',
                        'middle_name': u'',
                        'last_name': u'Jąder'
                    }
                ]
            }
        ),
        (
            {
                'authors': u'Małgorzata Żmudzka-Kosała'
            },
            {
                'authors': [
                    {
                        'name': u'Małgorzata Żmudzka-Kosała',
                        'first_name': u'Małgorzata',
                        'middle_name': u'',
                        'last_name': u'Żmudzka-Kosała'
                    }
                ]
            }
        ),
        (
            {
                'authors': u'Małgorzata Żmudzka - Kosała'
            },
            {
                'authors': [
                    {
                        'name': u'Małgorzata Żmudzka-Kosała',
                        'first_name': u'Małgorzata',
                        'middle_name': u'',
                        'last_name': u'Żmudzka-Kosała'
                    }
                ]
            }
        ),
        (
            {
                'authors': u'J.Kobuszewski'
            },
            {
                'authors': [
                    {
                        'name': u'J. Kobuszewski',
                        'first_name': 'J.',
                        'middle_name': u'',
                        'last_name': u'Kobuszewski'
                    }
                ]
            }
        ),
        (
            {
                'authors': u'S.J.Watson'
            },
            {
                'authors': [
                    {
                        'name': u'S. J. Watson',
                        'first_name': 'S.',
                        'middle_name': 'J.',
                        'last_name': u'Watson'
                    }
                ]
            }
        ),
        (
            {
                'authors': u'PIOTR CHOLEWIŃSKI'
            },
            {
                'authors': [
                    {
                        'name': u'PIOTR CHOLEWIŃSKI',
                        'first_name': u'Piotr',
                        'middle_name': u'',
                        'last_name': u'Cholewiński',
                    }
                ]
            }
        ),
        (
            {
                'authors': u'H.Łabonarska'
            },
            {
                'authors': [
                    {
                        'name': u'H. Łabonarska',
                        'first_name': u'H.',
                        'middle_name': u'',
                        'last_name': u'Łabonarska',
                    }
                ]
            }
        ),
        (
            {
                'authors': u'Wojciech Piotr  Kwiatek'
            },
            {
                'authors': [
                    {
                        'name': u'Wojciech Piotr Kwiatek',
                        'first_name': 'Wojciech',
                        'middle_name': 'Piotr',
                        'last_name': 'Kwiatek',
                    }
                ]
            }
        ),
        # TODO: T662
        # Stworzyć wsparcie dla mechanizmu rozróżniającego
        # faktyczne nazwiska autorów od np. nazw firm
        #
        # (
        #     {
        #         'authors': u'INFOA International s.r.o.'
        #     },
        #     {
        #         'authors': [
        #             {
        #                 'name': u'INFOA International s.r.o.'
        #             }
        #         ]
        #     }
        # ),
        (
            {
                'authors': u'Tomasz Martyniuk;Barbara Dudek;Monika Wąs'
            },
            {
                'authors': [
                    {
                        'name': u'Tomasz Martyniuk',
                        'first_name': u'Tomasz',
                        'middle_name': u'',
                        'last_name': u'Martyniuk',
                    },
                    {
                        'name': u'Barbara Dudek',
                        'first_name': u'Barbara',
                        'middle_name': u'',
                        'last_name': u'Dudek',
                    },
                    {
                        'name': u'Monika Wąs',
                        'first_name': u'Monika',
                        'middle_name': u'',
                        'last_name': u'Wąs',
                    }
                ]
            }
        ),
        (
            {
                'authors': u'Tomasz Martyniuk, Barbara Dudek, Monika Wąs'
            },
            {
                'authors': [
                    {
                        'name': u'Tomasz Martyniuk',
                        'first_name': u'Tomasz',
                        'middle_name': u'',
                        'last_name': u'Martyniuk',
                    },
                    {
                        'name': u'Barbara Dudek',
                        'first_name': u'Barbara',
                        'middle_name': u'',
                        'last_name': u'Dudek',
                    },
                    {
                        'name': u'Monika Wąs',
                        'first_name': u'Monika',
                        'middle_name': u'',
                        'last_name': u'Wąs',
                    }
                ]
            }
        ),
    )
    def test_validate_authors(self, args):
        self.validate_eq('Authors', *args)

    @data(
        (
            {
                'authors': u'Małgorzata Żmudzka-Kosała'
            },
            {
                'authors': [
                    {
                        'name': u'Małgorzata Żmudzka-Kosała',
                        'first_name': 'Małgorzata',
                        'middle_name': u'',
                        'last_name': u'Żmudzka-Kosała'}
                ]
            }
        ),
        (
            {
                'authors': u'Małgorzata Żmudzka - Kosała'
            },
            {
                'authors': [
                    {
                        'name': u'Małgorzata Żmudzka - Kosała',
                        'first_name': 'Małgorzata',
                        'middle_name': u'',
                        'last_name': u'Żmudzka - Kosała'
                    }
                ]
            }
        ),
        (
            {
                'authors': u'Małgorzata Żmudzka - Kosała'
            },
            {
                'authors': [
                    {
                        'name': u'Małgorzata Żmudzka - Kosała',
                        'first_name': u'Małgorzata',
                        'middle_name': u'',
                        'last_name': u'Żmudzka-Kosała'
                    }
                ]
            }
        ),
        (
            {
                'authors': u'Małgorzata Żmudzka - Kosała'
            },
            {
                'authors': [
                    {
                        'name': u'Małgorzata Żmudzka - Kosała'
                    }
                ]
            }
        ),
        # TODO: T661
        # Stworzyć wsparcie dla rozpoznawania tytułów naukowych
        # i innych w nazwiskach autorów, tłumaczy, etc.
        #
        # (
        #     {
        #         'authors': u'Red. Katarzyna Cymbalista-Hajib'
        #     },
        #     {
        #         'authors': [
        #             {
        #                 'middle_name': u'Katarzyna',
        #                 'last_name': u'Cymbalista-Hajib',
        #                 'name': u'Red. Katarzyna Cymbalista-Hajib',
        #                 'first_name': u'Red.',
        #             }
        #         ]
        #     }
        # ),
    )
    def test_validate_authors_not_eq(self, args):
        self.validate_not_eq('Authors', *args)
