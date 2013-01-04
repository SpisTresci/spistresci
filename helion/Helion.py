from generic import XMLConnector
from xml.etree import ElementTree as et
import os
import traceback

#TODO: translate helion xml tags into some kind of standarized key in dict
#TODO: what to do with more than one elements with the same tagname?
class Helion(XMLConnector):
    
    
    def __init__(self):
        url = 'http://helion.pl/xml/produkty-wszystkie.xml.zip'
        XMLConnector.__init__(self, url, XMLConnector.ZIPPED_XMLS)
        
    def parse(self):
                
        filename  = 'produkty-wszystkie/produkty-wszystkie.xml'
        if not os.path.exists(filename):
            exit(-1)
 
        root = et.parse(filename).getroot()
        for baza in root[:2]:
            for book in baza[:3]:
                book_dict = {}
                for elem in book:
#                    print "%s:%s"%(elem.tag,elem.text)
                    book_dict[elem.tag] = elem.text
                print book_dict
#            print "Tytul: ",book_dict['tytul']
#            print "ID: ", book_dict['ident']
#            print "Opis: ", book_dict['opis']
#            print "url: ",book_dict['link']
#            print 

   
