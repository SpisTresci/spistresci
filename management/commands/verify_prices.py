# -*- coding: utf-8 -*-

import urllib
import re
from datetime import datetime
from collections import defaultdict
from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings

from lxml import etree

from spistresci.common.helpers import send_email
from spistresci.models import Minibook


class Command(BaseCommand):

    number_of_books_per_shop = 20

    option_list = BaseCommand.option_list + (
        make_option('-e', '--email',
                    action='store_true',
                    dest='email_admins',
                    help='Notify all admins by sending email',
                    default=False),
    )

    bookstores = ['BezKartek', 'ZielonaSowa', 'Merlin', 'Legimi', 'Nexto',
        'Selkar', 'eBookpoint', 'Latarnik', 'Publio', 'Tmc', 'Czytio',
        'Allegro', 'Audioteka', 'Wikibooks', 'OnePress', 'Zantes', 'Bookoteka',
        'Koobe', 'BooksOn', 'Abooki', 'Gandalf', 'Virtualo', 'Helion',
        'KodeksyWmp3', 'Zinamon', 'WolneLektury', 'ebooks43', 'Bezdroza',
        'Audiobook', 'Audeo', 'DlaBystrzakow', 'Sensus', 'Fabryka',
        'FantastykaPolska', 'eClicto', 'TaniaKsiazka', 'DobryEbook', 'Wydaje',
        'Pokatne', 'Woblink', 'Septem', 'Ksiazki', 'ZloteMysli', 'Empik',
        'EscapeMagazine', 'CzeskieKlimaty', 'WolneEbooki']

    xpaths = {
        'BezKartek': "//span[@class='cena_price']/text()",
        'Selkar': "//span[@class='price']/text()",
        'Gandalf': "//span[@itemprop='price']/text()",
        "Zinamon": "//span[@class='cenaNew']/text()",
        "Virtualo": "//span[@class='price']/text()",

        # TODO
        #"Legimi": "//span[@itemprop='price']/text()",
        #"eClicto": "//span[@class='red strong fhuge']/text()",
    }

    def handle(self, *args, **options):
        self.errors = defaultdict(list)
        self.invalid_links = defaultdict(list)

        for bookstore, xpath in self.xpaths.iteritems():
            print bookstore
            minibooks = Minibook.objects.filter(bookstore=bookstore).order_by('?')[:self.number_of_books_per_shop]

            for book in minibooks:
                # url = urllib.quote(book.url.encode('utf8'))
                page_handler = urllib.urlopen(book.url)
                page_content = page_handler.read()

                parser = etree.HTMLParser()
                root = etree.XML(page_content, parser=parser)

                try:
                    price_str = root.xpath(xpath)[0]
                    price = int(''.join(re.findall(r'\d+', price_str)))
                except:
                    self.invalid_links[bookstore].append(book)
                    continue

                if book.price == price:
                    print '%s, cena ok' % book.title
                else:
                    error = dict(book=book, page_price=price)
                    self.errors[bookstore].append(error)
                    print '%s, cena na stronie %s, cena w bazie %s' % (book.title, price, book.price)

        self.print_errors()

    def print_errors(self):
        print '****************'
        print 'NIEPRAWIDLOWE CENY'
        for bookstore, errors in self.errors.iteritems():
            print bookstore
            for error in errors:
                print '%s (id: %s), cena w bazie: %s, cena na stronie %s' % (error['book'].url, error['book'].id, error['book'].price, error['page_price'])

        print '****************'
        print 'NIEPRAWIDLOWE LINKI'
        for bookstore, books in self.invalid_links.iteritems():
            print bookstore
            for book in books:
                print '(id: %s) %s' % (book.id, book.url)

    def send_errors(self):
        pass
