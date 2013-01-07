from generic import XMLConnector
import os
from xml.etree import ElementTree as et

class DobryEbook(XMLConnector):

    url = "http://dobryebook.pl/xml/spistresci.xml"

    def test(self):
        print "test"

    def __init__(self):
        XMLConnector.__init__(self, self.url, XMLConnector.SINGLE_XML)

    def parse(self):

        filename  = 'spistresci.xml'
        if not os.path.exists(filename):
            exit(-1)

        root = et.parse(filename).getroot()

        for ebook in root:
            title = ebook.find('tytul').text
            subtitle = ebook.find('podtytul').text
            author = ebook.find('autor').text
            link = ebook.find('link').text
            price = ebook.find('cena').text
            file_size = ebook.find('wielkosc_pliku').text
            numberOfPages = ebook.find('liczba_stron').text
            isbn = ebook.find('isbn').text
            smallCover = ebook.find('male_zdjecie').text
            bigCover = ebook.find('duze_zdjecie').text

            print "Tytul: " + title
            print "Autor: " + author
            print "Cena: " + price
            print "ISBN: " + isbn + "\n"

