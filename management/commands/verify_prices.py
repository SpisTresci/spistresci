# -*- coding: utf-8 -*-

import re
from datetime import datetime
from collections import defaultdict
from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import mail_admins
from django.template.loader import render_to_string

from lxml import etree
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException

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
        "Merlin": "//span[@class='price']/text()",
        "Legimi": "//span[@itemprop='price']/text()",
        "Tmc": '//span[@id="st_product_options-price-brutto"]/text()',
        'Audioteka': "//div[@id='ctl00_ctl00_ctl00_PageBody_PageBody_ContentPlaceHolder1_controlProductDescriptionMain_priceInfo']//div[@class='price']/text()",
        'Bookoteka': "//span[@class='price EBOOK']/text()",
        'Selkar': "//span[@class='price']/text()",
        'Gandalf': ["//p[@class='old_price_big']/span[@class='new_price']/text()",
            "//p[@class='new_price_big']/span[@itemprop='price']/text()"],
        "Zinamon": "//span[@class='cenaNew']/text()",
        "Virtualo": "//*[@id='product_right']/tr[2]/td[2]/span/text()",
        #"//table[@id='product_right']//span[@class='price'][1]/text()",

        "Bezdroza": "//div[@itemprop='price']/text()",
        "Septem": "//div[@itemprop='price']/text()",
        "Publio": "//div[@id='buyOptions']//ins/text()",
        "Nexto": "//div[@class='buybox-in issue']//strong[@class='price']/text()",
        "Wydaje": "//div[@itemprop='offerDetails']//big[@class='price-ebook']/text()",
        "eBookpoint": "//div[@itemprop='price']/text()",
        "Latarnik": "//td[@class='basket']//div[@class='price']//em/text()",
        "Czytio": "//div[@class='right']//span[@class='price']/text()",
        "Allegro": "//div[@class='book-price']/span/text()",
        "OnePress": "//div[@itemprop='price']/text()",
        "Zantes": "//div[@class='prices']//span[@class='price_now']/strong/text()",
        "Koobe": "//span[@itemprop='price']/text()",
        "BooksOn": "//div[@id='offer_prices_info']/div[3]/span/text()",
        "Abooki": "//div[@id='ProductFull']//div[@class='price']/text()",
        "Helion": "//div[@id='box_ebook']/div[@class='price']/span/text()",
        "KodeksyWmp3": "//div[@id='price_produsts_info']//span[@class='price_view_span']/span/text()",
        "Audiobook": "//span[@class='fprice_class']/text()",
        "DlaBystrzakow": "//div[@itemprop='price']/text()",
        'Sensus': "//div[@id='box_ebook']/div[@class='price']/span/text()",
        'Fabryka': "//*[@id='productBox']/div[2]/div[2]/p[2]/text()",
        'eClicto': "//div[@class='productPrice productsInfo']//span[@class='red strong fhuge']/text()",
        'TaniaKsiazka': "//span[@itemprop='price']/text()",
        'DobryEbook': [
            "//div[@class='wersjaElektro']/p[@class='cena']/text()",
            "//div[@class='wersjaElektro']/div[@class='promocja']/text()"
        ],
        'Woblink': "//div[@id='NCENA']/text()",
        'Ksiazki': [
            "//span[@class='newPrice new-price']/text()",
            "//span[@class='newPrice single-price']/text()"
        ],
        'ZloteMysli': [
            "//*[@id='product-info-top']/div/div[2]/div[3]/div[1]/p[1]/ins/text()",
            "//*[@id='product-info']/fieldset/div/div[1]/label/span/span/text()",
        ],
        'EscapeMagazine': "//span[@class='price_now']/strong/text()",
        'CzeskieKlimaty': "//span[@itemprop='price']/text()",

        # free ebooks
        "WolneLektury": "",
        "ebooks43": "",
        "Wikibooks": "",
        'FantastykaPolska': "",
        'Pokatne': "",
        'WolneEbooki': "",  # need login?

        "ZielonaSowa": '', # 404
        "Audeo": "",  # site is down: "przerwa techniczna"
        'Empik': "", # no urls id db
    }

    test_with_selenium = ['Abooki', 'Legimi', 'Tmc', 'Audioteka', 'KodeksyWmp3',
        'TaniaKsiazka']

    bookstore_urls = {
        'Abooki': 'www.abooki.pl',
        'Legimi': 'www.legimi.com',
        'Tmc': 'www.tmc.com.pl',
        'Audioteka': 'audioteka.pl',
        'KodeksyWmp3': 'www.kodeksywmp3.pl',
        'TaniaKsiazka': 'www.taniaksiazka.pl',
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
        self.driver = webdriver.Firefox()

        for bookstore in self.bookstores:
            print u'*'*40
            print bookstore
            xpath = self.xpaths.get(bookstore)
            minibooks = Minibook.objects.filter(bookstore=bookstore).exclude(url='').order_by('?')[:self.book_limit]

            for book in minibooks:
                print book.url

                if bookstore in self.test_with_selenium:
                    bookstore_url = self.bookstore_urls.get(bookstore, '')
                    page_content = self.get_page_content_with_selenium(book, bookstore, bookstore_url)
                else:
                    page_content = self.get_page_content(book, bookstore)

                if not page_content:
                    continue

                if not xpath:
                    continue

                price = self.fetch_price(page_content, bookstore)
                if price == None:
                    item = dict(book=book, reason=u"Nie można znaleźć ceny")
                    self.invalid_links[bookstore].append(item)
                    continue

                if book.price == price:
                    print u'%s, cena ok' % book.title
                else:
                    error = dict(book=book, page_price=price)
                    self.errors[bookstore].append(error)
                    print u'%s, cena na stronie %s, cena w bazie %s' % (book.title, price, book.price)

        self.print_errors()
        if self.email_admins:
            self.send_errors()
        self.driver.quit()

    def set_attributes(self, options):
        bookstore = options.get('bookstore')
        if bookstore:
            if not bookstore in self.xpaths.keys():
                print u'Bookstore name is invalid.'
                print u'Choices are: ' + ', '.join(self.xpaths.keys())
                return
            self.bookstores = [bookstore]
        else:
            self.bookstores = self.xpaths.keys()

        book_limit = options.get('number')
        if book_limit:
            self.book_limit = book_limit
        self.email_admins = options.get('email_admins')

    def get_page_content(self, book, bookstore):
        custom_session = getattr(self, 'get_%s_session' % bookstore.lower(), None)
        if custom_session:
            session = custom_session()
        else:
            session = requests.session()

        try:
            response = session.get(book.url)
        except Exception as inst:
            item = dict(book=book, reason=str(inst))
            self.invalid_links[bookstore].append(item)
            return

        print u'Status code:', response.status_code
        if response.status_code not in (200, 302):
            item = dict(book=book, reason="Status odpowiedzi: %s" % response.status_code)
            self.invalid_links[bookstore].append(item)
            return
        return response.content

    def get_nexto_session(self):
        session = requests.session()
        url = 'https://www.nexto.pl/klub/login.xml'
        data = {'remember': 0, 'password': 'pomyslowo42', 'extraParam': '',
            'email': 'mateusz.sikora@spistresci.pl', 'fb_form_id': 'login'}
        session.post(url, data=data)
        return session

    def get_page_content_with_selenium(self, book, bookstore, bookstore_url):

        def readystate_complete(d):
            return d.execute_script("return document.readyState") == "complete" and \
                bookstore_url in d.current_url
        try:
            self.driver.get(book.url)
            WebDriverWait(self.driver, 30).until(readystate_complete)
        except WebDriverException:
            pass
        elem = self.driver.find_element_by_xpath("//*")
        page_content = elem.get_attribute("outerHTML")
        return page_content

    def fetch_price(self, page_content, bookstore):
        parser = etree.HTMLParser()
        root = etree.XML(page_content, parser=parser)
        xpaths = self.xpaths.get(bookstore)
        if isinstance(xpaths, str):
            xpaths = [xpaths]
        price = None
        #import ipdb; ipdb.set_trace()
        for xpath in xpaths:
            try:
                price_str = ''.join(root.xpath(xpath))
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
        print u'*'*40
        print u'NIEPRAWIDLOWE CENY'
        if self.errors:
            for bookstore, errors in self.errors.iteritems():
                print bookstore
                for error in errors:
                    print u'%s (id: %s), cena w bazie: %s, cena na stronie %s' % (error['book'].url, error['book'].id, error['book'].price, error['page_price'])
        else:
            print u'brak'

        print u'*'*40
        print u'NIEPRAWIDLOWE LINKI'
        if self.invalid_links:
            for bookstore, items in self.invalid_links.iteritems():
                print bookstore
                for item in items:
                    print u'(id: %s) %s, powod: %s' % (item['book'].id, item['book'].url, item['reason'])
        else:
            print u'brak'

    def send_errors(self):
        if self.errors or self.invalid_links:

            bookstores = dict()
            for bookstore in set(self.errors.keys() + self.invalid_links.keys()):
                item = dict(errors=self.errors.get(bookstore, []),
                    invalid_links=self.invalid_links.get(bookstore, []))
                bookstores[bookstore] = item
            context = dict(bookstores=bookstores)
            message = render_to_string(self.template_name, context)
            mail_admins(u'Raport nieprawidłowych cen i linków', '', html_message=message)
