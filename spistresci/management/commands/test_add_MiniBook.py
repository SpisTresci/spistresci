# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from spistresci.model_controler import add_MiniBook
from spistresci.models import Bookstore

class Command(BaseCommand):

    def handle(self, *args, **options):
        bookstore, created = Bookstore.objects.get_or_create(**{'name':'Allegro', 'url': 'http://ebooki.allegro.pl/'})

        b1 = {
            'category': 'E-booki/Mlodziezowe',
            'publisher': 'Wydawnictwo e-bookowo',
            'description': {'description': 'testowy opis'},
            'title': 'Opowiesci o Malej Czarownicy Ismie',
            'url': u'http://ebooki.allegro.pl/ebook,b201.html',
            'b64_url': 'aHR0cDovL2Vib29raS5hbGxlZ3JvLnBsL2Vib29rLGIyMDEuaHRtbA==',
            'price': u'1520',
            'formats': [{'name': 'epub'}, {'name': 'mobi'}],
            'cover': u'http://ebooki.allegro.pl/imageshandler/201/miniature/',
            'authors': [{'middle_name': '', 'last_name': 'Ciepko', 'name': 'Aneta Ciepko', 'first_name': 'Aneta'}],
            #'book_type': None,
            'pp_url': u'http://www.a4b-tracking.com/pl/stat-click-text-link/56/120/aHR0cDovL2Vib29raS5hbGxlZ3JvLnBsL2Vib29rLGIyMDEuaHRtbA==',
            'isbns': [{'raw': u'9788362184409', 'valid': False, 'isbn10': u'8362184406', 'isbn13': u'9788362184409', 'core': u'836218440'}],
            'date': u'2012',
            'price_normal': u'-1',
            'external_id': u'219',
            'availability': u'1'
        }


        add_MiniBook(
            bookstore,
            b1
        )
        print 'end'