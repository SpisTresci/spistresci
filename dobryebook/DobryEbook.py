from generic import XMLConnector
import os
from xml.etree import ElementTree as et

class DobryEbook(XMLConnector):

    def __init__(self):
        XMLConnector.__init__(self)

    def parse(self):

        filename=os.path.join(self.backup_dir,self.filename)
        if not os.path.exists(filename):
            raise IOError('%s connector, missing xml file %s'%(self.my_name(),filename))

        root = et.parse(filename).getroot()

        for ebook in root:
            title = ebook.findtext('tytul', '')
            subtitle = ebook.findtext('podtytul', '')
            author = ebook.findtext('autor', '')
            link = ebook.findtext('link', '')
            price = ebook.findtext('cena', '')
            file_size = ebook.findtext('wielkosc_pliku', '')
            numberOfPages = ebook.findtext('liczba_stron', '')
            isbn = ebook.findtext('isbn', '')
            smallCover = ebook.findtext('male_zdjecie', '')
            bigCover = ebook.findtext('duze_zdjecie', '')

            print "Tytul: " + title
            print "Autor: " + author
            print "Cena: " + price
            print "ISBN: " + isbn + "\n"

