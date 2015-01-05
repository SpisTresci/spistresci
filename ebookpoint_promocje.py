# -*- coding: utf-8 -*-
from spistresci.models import *


ids_filename = '/home/noisy/devel/ebookpoint/ids.txt'




ids = []
with open(ids_filename) as file:
    for id in file:
        id = id.strip()
        ids.append(id)


w_promocji = MiniBook.objects.filter(external_id__in=ids)


kategorie_informatyczne = """
Serwery internetowe
Access
MySQL
Moodle
Elektronika
AJAX
Algorytmy
Asembler
Grafika komputerowa
Cisco
SQL
Wordpress
Nagrywanie płyt CD i DVD
PHP
Komputer w biurze
jQuery
Java
Linux
Excel
Techniki programowania
Funkcjonalność stron
Tworzenie stron WWW
HTML i XHTML
C
CSS
Turbo Pascal
C++
GIMP
C#
3ds max
Controlling
Budowa sieci
CAD/CAM
Konfiguracja sieci
Oracle
Programowanie
Hacking
Pozycjonowanie (SEO/SEM)
Sieci domowe
MathCad
Programowanie mobilne
PowerPoint
MS Office
Zarządzanie projektami IT
JavaScript
Podstawy obsługi komputera
Python
Drupal
Matematyka
Informatyka
BIOS
Elementy komputera
Bezpieczeństwo sieci
Web Design
Windows
Zarządzanie projektami
Flash/ActionScript
Mac OS
Joomla!
UML
PostgreSQL
J2EE - Programowanie
"""

kategorie_informatyczne = kategorie_informatyczne.split('\n')


informatyczne_ksiazki = []
for book in w_promocji:
    if any(them in kategorie_informatyczne for them in [them.strip() for them in book.extra['thematic_series'].split(',')]):
        book.title
        informatyczne_ksiazki.append(book)


date_dicts = [
    {
        'book':book,
        'ebook_date': book.extra['date'],
        'date': book.extra['date'],
        'external_id': book.external_id
    }
    for book in informatyczne_ksiazki
]


i = 0
for item in date_dicts:
    i += 1
    if item['external_id'].endswith('_EBOOK'):
        paper_book_external_id = item['external_id'].replace('_EBOOK', '')
        try:
            paper_book = MiniBook.objects.get(external_id=paper_book_external_id)
            item['paper_date'] = paper_book.extra['date']
            if paper_book.extra['date'] < item['date']:
                print "%d. %s: %s -> %s" % (i, item['book'].title, item['date'], paper_book.extra['date'])
                item['date'] = paper_book.extra['date']
            else:
                print "%d. %s: %s == %s" % (i, item['book'].title, item['date'], paper_book.extra['date'])

        except Exception, e:
            pass
