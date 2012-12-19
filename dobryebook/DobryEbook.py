from generic.XMLConnector import XMLConnector
import os
from xml.dom import minidom

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
        
        DOMTree = minidom.parse(filename)
        ebooks = DOMTree.childNodes.item(0).childNodes
        
        for ebook in ebooks:
            title = self.getTagValue(ebook, 'tytul')
            subtitle = self.getTagValue(ebook, 'podtytul')
            author = self.getTagValue(ebook, 'autor')
            link = self.getTagValue(ebook, 'link')
            price = self.getTagValue(ebook, 'cena')
            file_size = self.getTagValue(ebook, 'wielkosc_pliku')
            numberOfPages = self.getTagValue(ebook, 'liczba_stron')
            isbn = self.getTagValue(ebook, 'isbn')
            smallCover = self.getTagValue(ebook, 'male_zdjecie')
            bigCover = self.getTagValue(ebook, 'duze_zdjecie')
            
            print "Tytul: " + title
            print "Autor: " + author
            print "Cena: " + price
            print "ISBN: " + isbn + "\n"
            
            