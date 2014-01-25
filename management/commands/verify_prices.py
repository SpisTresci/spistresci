# -*- coding: utf-8 -*-

import urllib
import re
from datetime import datetime
from collections import defaultdict
from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import mail_admins
from django.template.loader import render_to_string

from lxml import etree

from spistresci.common.helpers import send_email
from spistresci.models import Minibook


class Command(BaseCommand):

    book_limit = 10
    template_name = 'email/prices_report.html'

    option_list = BaseCommand.option_list + (
        make_option('-e', '--email',
                    action='store_true',
                    dest='email_admins',
                    help='Notify all admins by sending email with report',
                    default=False),
        make_option('-b', '--bookstore',
                    action='store',
                    type="string",
                    dest='bookstore',
                    help='Name of bookstore to tests. If not given, all bookstores will be tested.'),
        make_option('-n', '--number',
                    action="store",
                    type="int",
                    dest="number",
                    help='Number of links per bookshop to be tested. Default 10.'),
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
        # ok

        "ZielonaSowa": '',
        # js redirection - return always 200
        # bookstore's page gives 404

        "Merlin": "//span[@class='price']/text()",

        "Legimi": '',
        "Tmc": '',
        'Audioteka': '',
        'Bookoteka': '',
        'Selkar': "//span[@class='price']/text()",
        'Gandalf': ["//p[@class='old_price_big']/span[@class='new_price']/text()",
            "//p[@class='new_price_big']/span[@itemprop='price']/text()"],
        "Zinamon": "//span[@class='cenaNew']/text()",
        "Virtualo": "//span[@class='price']/text()",
        "Bezdroza": "//div[@itemprop='price']/text()",
        "Septem": "//div[@itemprop='price']/text()",
        "Publio": "//div[@id='buyOptions']//ins/text()",
        "Nexto": "//strong[@class='price']/text()",
        "Wydaje": "//div[@itemprop='offerDetails']//big[@class='price-ebook']/text()",
        "eBookpoint": "//div[@itemprop='price']/text()",
        "Latarnik": "//td[@class='basket']//div[@class='price']//em/text()",
        "Czytio": "//span[@class='price']/text()",
        "Allegro": "//div[@class='book-price']/span/text()",
        "Wikibooks": "",  # free ebooks
        "OnePress": "//div[@itemprop='price']/text()",
        "Zantes": "//span[@class='price_now']/strong/text()",
        "Koobe": "//span[@itemprop='price']/text()",
        "BooksOn": "",  # no valid links in db?
        "Abooki": "",  # js redirection? "//div[@class='price']/text()",
        "Helion": "//div[@id='box_ebook']/div[@class='price']/span/text()",
        "KodeksyWmp3": "",  # js redirection? //span[@class='price_view_span']/span/text()
        "WolneLektury": "",  # site is down
        "ebooks43": "",  # free ebooks
        "Audiobook": "",  # no valid links in db?
        "Audeo": "",  # no valid links in db?
        "DlaBystrzakow": "",
        'Sensus': "//div[@id='box_ebook']/div[@class='price']/span/text()",
        'Fabryka': "//p[@class='new-price']/text()",
        'FantastykaPolska': "",  # free ebooks?
        'eClicto': "",  # special characters in urls
        'TaniaKsiazka': "",  # js redirection?
        'DobryEbook': ["//div[@class='wersjaElektro']/p[@class='cena']/text()",
            "//div[@class='wersjaElektro']/div[@class='promocja']/text()"],
        'Pokatne': "",  # free ebooks?
        'Woblink': "//div[@id='NCENA']/text()",
        'Ksiazki': ["//span[@class='newPrice new-price']/text()",
            "//span[@class='newPrice single-price']/text()"],
        'ZloteMysli': "//p[@class='price']/ins/text()",
        'Empik': "",
        'EscapeMagazine': "//span[@class='price_now']/strong/text()",
        'CzeskieKlimaty': "",  # invalid links in db?
        'WolneEbooki': "",
    }

    # extra converters for price fetch from bookstore's pages
    price_converters = {
        "Wydaje": lambda x: x.replace(',-', ',00'),
        "Merlin": lambda x: x if ',' in x else str(x)+'00'
    }

    def handle(self, *args, **options):
        self.set_attributes(options)

        self.errors = defaultdict(list)
        self.invalid_links = defaultdict(list)

        for bookstore in self.bookstores:
            print '*'*40
            print bookstore
            xpath = self.xpaths.get(bookstore)
            minibooks = Minibook.objects.filter(bookstore=bookstore).order_by('?')[:self.book_limit]

            for book in minibooks:
                print book.url
                try:
                    page_handler = urllib.urlopen(book.url)
                except:
                    self.invalid_links[bookstore].append(book)
                    continue
                print 'Status code:', page_handler.getcode()
                if page_handler.getcode() not in (200, 302):
                    self.invalid_links[bookstore].append(book)
                    continue

                if not xpath:
                    continue

                page_content = page_handler.read()
                price = self.fetch_price(page_content, bookstore)

                if price == None:
                    self.invalid_links[bookstore].append(book)
                    continue

                if book.price == price:
                    print '%s, cena ok' % book.title
                else:
                    error = dict(book=book, page_price=price)
                    self.errors[bookstore].append(error)
                    print '%s, cena na stronie %s, cena w bazie %s' % (book.title, price, book.price)

        self.print_errors()
        if self.email_admins:
            self.send_errors()

    def set_attributes(self, options):
        bookstore = options.get('bookstore')
        if bookstore:
            if not bookstore in self.xpaths.keys():
                print 'Bookstore name is invalid.'
                print 'Choices are: ' + ', '.join(self.xpaths.keys())
                return
            self.bookstores = [bookstore]
        else:
            self.bookstores = self.xpaths.keys()

        book_limit = options.get('number')
        if book_limit:
            self.book_limit = book_limit
        self.email_admins = options.get('email_admins')

    def fetch_price(self, page_content, bookstore):
        parser = etree.HTMLParser()
        root = etree.XML(page_content, parser=parser)
        xpaths = self.xpaths.get(bookstore)
        if isinstance(xpaths, str):
            xpaths = [xpaths]
        price = None

        for xpath in xpaths:
            try:
                price_str = root.xpath(xpath)[0]
                price_converter = self.price_converters.get(bookstore)
                if price_converter:
                    price_str = price_converter(price_str)
                price = int(''.join(re.findall(r'\d+', price_str)))
                return price
            except:
                # can't find price, seems link is invalid
                continue
        return price

    def print_errors(self):
        print '*'*40
        print 'NIEPRAWIDLOWE CENY'
        if self.errors:
            for bookstore, errors in self.errors.iteritems():
                print bookstore
                for error in errors:
                    print '%s (id: %s), cena w bazie: %s, cena na stronie %s' % (error['book'].url, error['book'].id, error['book'].price, error['page_price'])
        else:
            print 'brak'

        print '*'*40
        print 'NIEPRAWIDLOWE LINKI'
        if self.invalid_links:
            for bookstore, books in self.invalid_links.iteritems():
                print bookstore
                for book in books:
                    print '(id: %s) %s' % (book.id, book.url)
        else:
            print 'brak'

    def send_errors(self):
        if self.errors or self.invalid_links:
            context = dict(errors=dict(self.errors),
                invalid_links=dict(self.invalid_links))
            message = render_to_string(self.template_name, context)
            mail_admins(u'Raport nieprawidłowych cen i linków', '', html_message=message)
