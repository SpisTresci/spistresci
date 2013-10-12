# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from spistresci.auth.views import authorization
from spistresci.constants import *
from spistresci.filters.filters import *
from constants import *

def book(request, book_id):
    c = {'top_menu':getListOfTopMenuServices(request)}
    c.update({'path':request.path})
    authorization(request, c)
    c['request'] = request
    c['book'] = get_book(book_id)

    c['filters'] = [
                            {
                                'name':'SERWISY',
                                'name_id':'services',
                                'template_file':'book_filter_list_form.html',
                                'data': loadFilterState(None, {'Wszystkie':['Abook', ' Audeo', ' Audiobook', ' Audioteka', ' Bezdroza','Abooki', ' Audeo', ' Audiobook', ' Audioteka', ' Bezdroza', ' BezKartek']}, "services")
                            },
                            {
                                'name':'FORMATY',
                                'name_id':'formats',
                                'template_file':'book_filter_list.html',
                                'data':loadFilterState(None, supported_formats, "formats")
                            },
                            {
                                'name':'',
                                'name_id':'services',
                                'template_file':'book_filter_list.html',
                                'data': loadFilterState(None, {}, "services")
                            },
                            {
                                'name':'SPOSÓB PŁATNOŚCI',
                                'name_id':'formats',
                                'template_file':'book_filter_list.html',
                                'data':loadFilterState(None, {"Przez serwis":["DotPay", "ePrzelewy", "PayU", "Przelewy24.pl", "transferuj.pl", "YetiPay", "mPay", "SkyCash", "SMS", "PayPal", "karty płatnicze", "Przelewy24.pl"]}, "formats")
                            },
                            {
                                'name':'SERWISY',
                                'name_id':'services',
                                'template_file':'book_filter_list.html',
                                'data': loadFilterState(None, {'Wszystkie':['Abooki', ' Audeo', ' Bezdroza', ' BezKartek']}, "services")
                            },
#                            {
#                                'name':'CENA',
#                                'name_id':'price',
#                                'template_file':'book_filter_price.html',
#                                'data':self.loadFilterPriceState(['from', 'to'])
#                            },
                   ]

    c['result']={
    "title":u'Futbol jest okrutny',
    "cover":u'http://www.koobe.pl/static/28/28999/img/7e0209b390cee04a157b5e5ffdf754d6_226_0_n_100/145390.jpg',
    "records":
        [
            {'format_mp3': False, 'format_cd': False, 'url': u'http://www.koobe.pl/1340589,ebook,futbol-jest-okrutny.htm?utm_source=ekundelek&utm_medium=porownywarki&utm_campaign=porownywarki', 'price': '27.90', 'cover': u'http://www.koobe.pl/static/28/28999/img/7e0209b390cee04a157b5e5ffdf754d6_226_0_n_100/145390.jpg', 'format_mobi': True, 'bookstore': u'Koobe', 'format_pdf': False, 'formats': ['MOBI', 'EPUB'], 'format_epub': True}
            ,
            {'format_mp3': False, 'format_cd': False, 'url': u'http://virtualo.pl/futbol_jest_okrutny/i129008/', 'price': '25.60', 'cover': u'http://static.virtualo.pl/media_images/normal/145390.jpg', 'format_mobi': False, 'bookstore': u'Virtualo', 'format_pdf': False, 'formats': ['EPUB'], 'format_epub': True}
            ,
            {'format_mp3': False, 'format_cd': False, 'url': u'http://virtualo.pl/futbol_jest_okrutny/i129020/', 'price': '25.60', 'cover': u'http://static.virtualo.pl/media_images/normal/145424.jpg', 'format_mobi': True, 'bookstore': u'Virtualo', 'format_pdf': False, 'formats': ['MOBI'], 'format_epub': False}
            ,
            {'format_mp3': False, 'format_cd': False, 'url': u'http://ebookpoint.pl/ksiazki/futbol-jest-okrutny-michal-okonski,e_201f_ebook.htm', 'price': '27.90', 'cover': u'http://ebookpoint.pl/okladki/326x466/e_201f.jpg', 'format_mobi': True, 'bookstore': u'eBookpoint', 'format_pdf': True, 'formats': ['MOBI', 'PDF', 'EPUB'], 'format_epub': True}
        ],

    "name":[u'Michał Okoński'],
    "formats":['PDF', 'MOBI', 'EPUB'],
    "services":[u'Virtualo', u'eBookpoint', u'Koobe'],
    "price_lowest":'25.60',
    "filtered_records_number":2,
    "price_lowest_before_filtering":'10.00',
    "filtered_formats":['PDF', 'MOBI', 'EPUB'],
    }

    return render_to_response('book.html', c)

def book_description(request, book_id):
    return HttpResponse(get_book_description(book_id))

def get_book(book_id):
    #TODO: we have only 3 random books now.
    import random
    book_id = random.choice(['kilka', 'szkolne', 'aby'])
    return books.get(book_id, {})

def get_book_description(book_id):
    #TODO: we have only 3 random books now.
    import random
    book_id = random.choice(['kilka', 'szkolne', 'aby'])
    return book_descriptions[book_id]